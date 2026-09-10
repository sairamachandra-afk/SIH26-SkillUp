document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('cardNavToggle');
  const dropdown = document.getElementById('cardNavDropdown');
  const cards = dropdown ? dropdown.querySelectorAll('.nav-card') : [];
  const dockItems = document.querySelectorAll('.dock-item');
  const dockNav = document.getElementById('dockNav');

  let isExpanded = false;

  if (dropdown) {
    gsap.set(dropdown, {
      scale: 0.94,
      opacity: 0,
      y: -8,
      display: 'none'
    });
    gsap.set(cards, { y: 24, opacity: 0 });
  }

  const openDropdown = () => {
    if (!dropdown) return;
    isExpanded = true;
    toggleBtn.classList.add('open');

    gsap.killTweensOf([dropdown, cards]);
    gsap.set(dropdown, { display: 'flex' });

    gsap.to(dropdown, {
      scale: 1,
      opacity: 1,
      y: 0,
      duration: 0.35,
      ease: 'power3.out'
    });

    gsap.to(cards, {
      y: 0,
      opacity: 1,
      duration: 0.3,
      stagger: 0.06,
      ease: 'power3.out',
      delay: 0.05
    });
  };

  const closeDropdown = () => {
    if (!dropdown) return;
    isExpanded = false;
    toggleBtn.classList.remove('open');

    gsap.killTweensOf([dropdown, cards]);

    gsap.to(cards, {
      y: 12,
      opacity: 0,
      duration: 0.2,
      stagger: 0.03,
      ease: 'power2.in'
    });

    gsap.to(dropdown, {
      scale: 0.94,
      opacity: 0,
      y: -8,
      duration: 0.25,
      ease: 'power2.in',
      delay: 0.05,
      onComplete: () => {
        gsap.set(dropdown, { display: 'none' });
      }
    });
  };

  if (toggleBtn && dropdown) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!isExpanded) {
        openDropdown();
      } else {
        closeDropdown();
      }
    });

    document.addEventListener('click', (e) => {
      if (isExpanded && !dropdown.contains(e.target) && !toggleBtn.contains(e.target)) {
        closeDropdown();
      }
    });
  }

  if (dockNav && dockItems.length > 0) {
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

          gsap.to(item, {
            scale: targetScale,
            duration: 0.25,
            ease: 'power2.out',
            overwrite: 'auto'
          });
        } else {
          gsap.to(item, {
            scale: minScale,
            duration: 0.3,
            ease: 'power2.out',
            overwrite: 'auto'
          });
        }
      });
    });

    dockNav.addEventListener('mouseleave', () => {
      dockItems.forEach((item) => {
        gsap.to(item, {
          scale: minScale,
          duration: 0.35,
          ease: 'power2.out',
          overwrite: 'auto'
        });
      });
    });
  }
});