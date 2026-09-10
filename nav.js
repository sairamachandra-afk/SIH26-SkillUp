document.addEventListener('DOMContentLoaded', () => {
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

  document.querySelectorAll('a.login-link, a#signOutBtn, button#signOutBtn, .sign-out-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      localStorage.removeItem('skillup_user');
      localStorage.removeItem('skillup_active_user');
      sessionStorage.clear();
      if (window.location.protocol === 'file:') {
        window.location.href = window.location.pathname.includes('Templates') ? 'index.html' : 'Templates/index.html';
      } else {
        window.location.href = '/logout';
      }
    });
  });
});