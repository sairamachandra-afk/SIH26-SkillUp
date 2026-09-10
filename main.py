from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "sih-skillup-secret-key-national-intelligence"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

app = FastAPI(title="SkillUp Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_DB = {
    "trainee@skillup.gov.in": {
        "id": "TRN-2026-891",
        "name": "Rahul Sharma",
        "email": "trainee@skillup.gov.in",
        "password": "password123",
        "role": "trainee",
        "batch": "PMKVY Data Analytics 2025",
        "skills": ["Python", "SQL", "Excel"]
    },
    "admin@msde.gov.in": {
        "id": "ADM-HQ-01",
        "name": "Dr. Ananya Iyer",
        "email": "admin@msde.gov.in",
        "password": "password123",
        "role": "admin",
        "department": "Ministry of Skill Development & Entrepreneurship",
        "region": "National HQ"
    },
    "recruiter@tcs.com": {
        "id": "EMP-TCS-402",
        "name": "Vikram Malhotra",
        "email": "recruiter@tcs.com",
        "password": "password123",
        "role": "employer",
        "company": "Tata Consultancy Services",
        "openings": 14
    }
}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    identifier: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/auth/login", response_model=TokenResponse)
def login(creds: LoginRequest):
    user = USERS_DB.get(creds.email)
    
    if not user or user["password"] != creds.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Try our pre-filled demo accounts."
        )
    
    if user["role"] != creds.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User is registered as a {user['role'].upper()}, not {creds.role.upper()}."
        )

    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    user_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "metadata": user.get("batch") or user.get("department") or user.get("company")
    }

    return {"access_token": access_token, "token_type": "bearer", "user": user_data}

@app.post("/api/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest):
    if req.email in USERS_DB:
        raise HTTPException(status_code=400, detail="User already registered.")

    new_id = f"{req.role[:3].upper()}-{datetime.utcnow().strftime('%M%S')}"
    new_user = {
        "id": new_id,
        "name": req.name,
        "email": req.email,
        "password": req.password,
        "role": req.role,
        "metadata": req.identifier or "General"
    }
    USERS_DB[req.email] = new_user

    access_token = create_access_token(
        data={"sub": new_user["email"], "role": new_user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer", "user": new_user}

@app.get("/api/auth/me")
def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None or email not in USERS_DB:
            raise HTTPException(status_code=401, detail="Invalid session token.")
        user = USERS_DB[email]
        return {"user": user}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)