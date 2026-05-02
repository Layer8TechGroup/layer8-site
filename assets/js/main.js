/* Layer8 Tech Group — Main JS */

// ── Mobile nav toggle ────────────────────────────────────────
const hamburger = document.querySelector('.hamburger');
const navLinks  = document.querySelector('.nav-links');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    const isOpen = navLinks.classList.contains('open');
    spans[0].style.transform = isOpen ? 'rotate(45deg) translate(5px, 5px)' : '';
    spans[1].style.opacity   = isOpen ? '0' : '1';
    spans[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px, -5px)' : '';
  });
}

// ── Dropdown on click (mobile-safe) ─────────────────────────
document.querySelectorAll('.nav-dropdown > a').forEach(btn => {
  btn.addEventListener('click', e => {
    const parent = btn.closest('.nav-dropdown');
    const isOpen = parent.classList.contains('open');
    // close all others
    document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
    if (!isOpen) {
      parent.classList.add('open');
      e.preventDefault();
    }
  });
});

document.addEventListener('click', e => {
  if (!e.target.closest('.nav-dropdown')) {
    document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
  }
});

// ── Active nav link ──────────────────────────────────────────
(function() {
  const path = window.location.pathname.replace(/\/$/, '');
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href') || '';
    const hrefClean = href.replace(/\/$/, '');
    if (hrefClean && path === hrefClean) a.classList.add('active');
    if (hrefClean && path.startsWith(hrefClean) && hrefClean !== '') {
      a.classList.add('active');
    }
  });
})();

// ── Smooth scroll for anchor links ──────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const navH = document.querySelector('.nav')?.offsetHeight || 64;
      const top  = target.getBoundingClientRect().top + window.scrollY - navH - 12;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── Scroll-triggered fade-in ─────────────────────────────────
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
} else {
  // Fallback: show all immediately
  document.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
}
