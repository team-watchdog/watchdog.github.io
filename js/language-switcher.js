document.addEventListener('DOMContentLoaded', () => {
  const langButtons = document.querySelectorAll('.lang-btn');
  const storedLang = localStorage.getItem('preferred-language') || 'en';

  // Set active state
  langButtons.forEach(btn => {
    if (btn.dataset.lang === storedLang) {
      btn.classList.add('lang-active');
    }
  });

  // Handle clicks
  langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      const currentUrl = new URL(window.location);
      currentUrl.searchParams.set('lang', lang);
      localStorage.setItem('preferred-language', lang);

      // Redirect to same page with lang param
      window.location.href = currentUrl.toString();
    });
  });
});
