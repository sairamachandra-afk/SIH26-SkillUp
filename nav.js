// ==========================================
// SkillUp Common Navigation System (nav.js)
// Single Source of Truth for Top Navigation Bar
// ==========================================

function initCommonSkillUpNavbar() {
  // Do not overwrite dock navigation on index.html landing page
  if (document.getElementById('dockNav')) {
    return;
  }

  const currentPath = window.location.pathname.toLowerCase();

  // Active page detection (handles both /workforce and /workforce.html, etc.)
  const isDashboard = currentPath.includes('dashboard');
  const isWorkforce = currentPath.includes('workforce');
  const isSkillGaps = currentPath.includes('skillgaps');
  const isEmployment = currentPath.includes('employ');

  // Relative prefix if opened via file:// or nested path
  const isNested = window.location.pathname.includes('/Templates/');
  const prefix = isNested ? '../' : '';

  const dashboardUrl = prefix + 'Dashboard.html';
  const workforceUrl = prefix + 'workforce.html';
  const skillgapsUrl = prefix + 'skillgaps.html';
  const employmentUrl = prefix + 'Employement.html';
  const homeUrl = prefix + 'index.html';

  const commonNavbarHTML = `
    <div class="w-full px-6 md:px-10 h-20 flex items-center justify-between gap-6">
      <div class="flex-shrink-0">
        <a href="${homeUrl}" class="flex items-center gap-3 group">
          <span class="text-brand-cyan text-2xl leading-none transition-transform group-hover:scale-110 duration-200">&#x25C9;</span>
          <span class="font-bold text-xl tracking-tight text-white">SkillUp</span>
        </a>
      </div>

      <nav class="hidden md:flex items-center justify-center gap-8 flex-1" id="skillupPortalNav">
        <a href="${dashboardUrl}" class="text-xs lg:text-sm font-medium ${isDashboard ? 'text-brand-cyan' : 'text-slate-300 hover:text-brand-cyan'} transition-colors">Dashboard Hub</a>
        <a href="${workforceUrl}" class="text-xs lg:text-sm font-medium ${isWorkforce ? 'text-brand-cyan' : 'text-slate-300 hover:text-brand-cyan'} transition-colors">Career Outcomes</a>
        <a href="${skillgapsUrl}" class="text-xs lg:text-sm font-medium ${isSkillGaps ? 'text-brand-cyan' : 'text-slate-300 hover:text-brand-cyan'} transition-colors">Skill Gaps</a>
        <a href="${employmentUrl}" class="text-xs lg:text-sm font-medium ${isEmployment ? 'text-brand-cyan' : 'text-slate-300 hover:text-brand-cyan'} transition-colors">Employment</a>
      </nav>

      <div class="flex items-center gap-3">
        <a href="/logout" id="skillupSignOutBtn" class="text-xs text-rose-400 hover:underline">Sign Out</a>
      </div>
    </div>
  `;

  let header = document.querySelector('header');
  if (header) {
    header.className = "sticky top-0 z-50 bg-brand-dark/80 backdrop-blur-xl border-b border-brand-border w-full";
    header.innerHTML = commonNavbarHTML;
  }
}

// Initialize navbar immediately if DOM ready, else on DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCommonSkillUpNavbar);
} else {
  initCommonSkillUpNavbar();
}

document.addEventListener('DOMContentLoaded', () => {
  // Ensure common navbar is initialized
  initCommonSkillUpNavbar();

  // Landing page Card Navigation toggle & GSAP animations
  const toggleBtn = document.getElementById('cardNavToggle');
  const dropdown = document.getElementById('cardNavDropdown');

  if (toggleBtn && dropdown) {
    const cards = dropdown.querySelectorAll('.nav-card');
    let isExpanded = false;
    dropdown.style.display = 'none';

    const openDropdown = () => {
      isExpanded = true;
      toggleBtn.classList.add('open');
      dropdown.style.display = 'flex';
      if (window.gsap) {
        gsap.killTweensOf([dropdown, cards]);
        gsap.fromTo(dropdown, { scale: 0.94, opacity: 0, y: -8 }, { scale: 1, opacity: 1, y: 0, duration: 0.3, ease: 'power3.out' });
        gsap.fromTo(cards, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, stagger: 0.05, ease: 'power3.out', delay: 0.05 });
      } else {
        dropdown.style.opacity = '1';
      }
    };

    const closeDropdown = () => {
      isExpanded = false;
      toggleBtn.classList.remove('open');
      if (window.gsap) {
        gsap.killTweensOf([dropdown, cards]);
        gsap.to(dropdown, {
          scale: 0.94, opacity: 0, y: -8, duration: 0.2, ease: 'power2.in',
          onComplete: () => { dropdown.style.display = 'none'; }
        });
      } else {
        dropdown.style.display = 'none';
      }
    };

    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!isExpanded) openDropdown();
      else closeDropdown();
    });

    document.addEventListener('click', (e) => {
      if (isExpanded && !dropdown.contains(e.target) && !toggleBtn.contains(e.target)) {
        closeDropdown();
      }
    });
  }

  // Landing page dock animation
  const dockNav = document.getElementById('dockNav');
  const dockItems = document.querySelectorAll('.dock-item');
  if (dockNav && dockItems.length > 0 && window.gsap) {
    const proximity = 120;
    const maxScale = 1.1;
    const minScale = 1;

    dockNav.addEventListener('mousemove', (e) => {
      const mouseX = e.clientX;
      dockItems.forEach((item) => {
        const rect = item.getBoundingClientRect();
        const itemCenterX = rect.left + rect.width / 2;
        const dist = Math.abs(mouseX - itemCenterX);
        if (dist < proximity) {
          const factor = 1 - dist / proximity;
          const targetScale = minScale + (maxScale - minScale) * factor;
          gsap.to(item, { scale: targetScale, duration: 0.25, ease: 'power2.out', overwrite: 'auto' });
        } else {
          gsap.to(item, { scale: minScale, duration: 0.3, ease: 'power2.out', overwrite: 'auto' });
        }
      });
    });

    dockNav.addEventListener('mouseleave', () => {
      dockItems.forEach((item) => {
        gsap.to(item, { scale: minScale, duration: 0.35, ease: 'power2.out', overwrite: 'auto' });
      });
    });
  }

  // Unified Sign Out listener
  document.querySelectorAll('a[href="/logout"], a#skillupSignOutBtn, a.login-link, a#signOutBtn, button#signOutBtn, .sign-out-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      localStorage.removeItem('skillup_user');
      localStorage.removeItem('skillup_active_user');
      sessionStorage.clear();
      if (window.location.protocol === 'file:') {
        e.preventDefault();
        window.location.href = window.location.pathname.includes('Templates') ? 'index.html' : 'Templates/index.html';
      }
      // Otherwise allow standard HTTP redirect to /logout
    });
  });
});