import os
import sqlite3
from datetime import timedelta
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

load_dotenv()

app = FastAPI(title="SkillUp Intelligence & Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key='skillup-portal-super-secret-key')

app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="Templates")

DB_NAME = 'database.db'
client = genai.Client(api_key='AQ.Ab8RN6IeIKvLSWn9AQ37OYEB86mRIP6lLC5gZMDMirs6ApUlYA')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            fullname TEXT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

    default_presets = [
        ('student', 'Trainee Alex', 'TRN-2026-001', 'trainee@skillup.gov.in', 'password123'),
        ('govt', 'Director Sairam', 'MSDE-DIR-901', 'officer@skillup.gov.in', 'govpass2026'),
        ('employer', 'HR Manager', 'DELOITTE-REC', 'recruiter@deloitte.com', 'hirepass2026')
    ]
    for role, fullname, username, email, raw_pw in default_presets:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO users (role, fullname, username, email, password) VALUES (?, ?, ?, ?, ?)',
                (role, fullname, username, email, generate_password_hash(raw_pw))
            )
    conn.commit()
    conn.close()

init_db()

@app.post("/api/analyze-resume")
async def analyze_resume(
    target_role: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF resumes are accepted.")
    
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)
        resume_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from uploaded PDF.")
            
    except Exception as e:
        print(f"PDF Parse Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")

    prompt = f"""
    You are an expert AI Career and Skill Intelligence Evaluator.
    Analyze the following candidate resume text against the target role: "{target_role}".
    
    Return a strict JSON object matching this exact schema:
    {{
      "readiness_score": <integer percentage between 0 and 100>,
      "matched_skills": [<array of string skills found in resume relevant to target role>],
      "missing_skills": [<array of critical string skills missing for target role>],
      "learning_roadmap": [
        {{
          "milestone": "<string title of milestone>",
          "time_estimate": "<string duration like '2 Weeks'>",
          "key_topics": [<array of string subtopics>]
        }}
      ]
    }}

    Resume Content:
    {resume_text[:4000]}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        
        # FIX: Clean the response text in case Gemini wraps it in ```json ... ``` markdown
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
        
    except Exception as e:
        print(f"LLM Error: {e}") # This prints the exact failure reason to your terminal
        raise HTTPException(status_code=500, detail=f"LLM Processing Error: {str(e)}")

@app.get('/')
@app.get('/index.html')
@app.get('/Templates/index.html')
async def home(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse(
        request=request, 
        name='index.html', 
        context={'request': request, 'user': user}
    )

@app.get('/login')
@app.get('/login.html')
@app.get('/Templates/login.html')
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name='login.html', 
        context={'request': request}
    )

@app.post('/auth/register')
async def auth_register(request: Request):
    form = await request.form()
    role = form.get('role', 'student')
    fullname = form.get('fullname', '').strip()
    username = form.get('username', '').strip()
    email = form.get('email', '').strip()
    password = form.get('password', '')

    if not username or not email or not password:
        return RedirectResponse(url='/login.html?mode=signup&error=missing_fields', status_code=303)

    hashed_pw = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (role, fullname, username, email, password) VALUES (?, ?, ?, ?, ?)',
            (role, fullname, username, email, hashed_pw)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return RedirectResponse(url='/login.html?mode=signup&error=already_exists', status_code=303)
    finally:
        conn.close()

    request.session['user'] = {'username': username, 'email': email, 'role': role, 'fullname': fullname}

    if role == 'govt':
        return RedirectResponse(url='/dashboard', status_code=303)
    elif role == 'employer':
        return RedirectResponse(url='/employment', status_code=303)
    return RedirectResponse(url='/skillgaps', status_code=303)

@app.post('/auth/login')
async def auth_login(request: Request):
    form = await request.form()
    role = form.get('role', 'student')
    identifier = form.get('identifier', '').strip()
    password = form.get('password', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE (username = ? OR email = ?) AND role = ?',
        (identifier, identifier, role)
    )
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        request.session['user'] = {'username': user['username'], 'email': user['email'], 'role': user['role']}
        if role == 'govt':
            return RedirectResponse(url='/dashboard', status_code=303)
        elif role == 'employer':
            return RedirectResponse(url='/employment', status_code=303)
        return RedirectResponse(url='/skillgaps', status_code=303)

    return RedirectResponse(url='/login.html?error=invalid_credentials', status_code=303)

@app.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url='/login.html', status_code=303)

@app.get('/dashboard')
@app.get('/Dashboard.html')
async def dashboard():
    return FileResponse("Dashboard.html")

@app.get('/workforce')
@app.get('/workforce.html')
async def workforce():
    return FileResponse("workforce.html")

@app.get('/skillgaps')
@app.get('/skillgaps.html')
async def skillgaps():
    return FileResponse("skillgaps.html")

@app.get('/employment')
@app.get('/Employement.html')
async def employment():
    return FileResponse("Employement.html")

@app.get('/{filename:path}')
async def serve_static(filename: str):
    if os.path.exists(filename) and os.path.isfile(filename):
        return FileResponse(filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/curate-resources")
async def curate_resources(request: Request):
    body = await request.json()
    milestone = body.get("milestone")
    key_topics = body.get("key_topics", [])
    
    prompt = f"""
    You are an expert technical education advisor and career intelligence evaluator.
    For the upskilling roadmap milestone "{milestone}" covering the key topics: {key_topics},
    provide 3 high-quality, practical learning resources (e.g., official documentation, free courses, or tutorials).
    
    Return a strict JSON array matching this exact schema:
    [
      {{
        "type": "<Documentation | Free Course | YouTube Tutorial | Article>",
        "title": "<Resource Title>",
        "url": "<Valid learning resource URL>",
        "description": "<1-sentence description of why it helps close this specific skill gap>"
      }}
    ]
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        return json.loads(raw_text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resource Curation Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)