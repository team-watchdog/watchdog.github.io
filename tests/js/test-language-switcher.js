// Language switcher should redirect when clicked
test('click language button updates URL and stores preference', async () => {
  localStorage.clear();
  const langBtn = document.querySelector('[data-lang="si"]');
  langBtn.click();
  expect(localStorage.getItem('preferred-language')).toBe('si');
  expect(window.location.href).toContain('lang=si');
});
