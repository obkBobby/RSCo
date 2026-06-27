const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// Preview-safe lead forms.
// Replace data-kit-placeholder forms with real Kit embeds before production launch.
document.querySelectorAll('form[data-kit-placeholder]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = form.querySelector('.form-message');
    const email = form.querySelector('input[type="email"]')?.value?.trim();
    const guide = form.getAttribute('data-kit-placeholder') || 'this guide';
    if (!email) return;
    if (message) {
      message.textContent = `Preview captured ${email} for ${guide}. Replace this form with the live Kit embed before launch.`;
      message.classList.add('is-visible');
    }
  });
});
