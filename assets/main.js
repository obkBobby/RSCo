const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

document.querySelectorAll('form.kit-live-form').forEach((form) => {
  const guide = form.querySelector('input[name="form-name"]')?.value || 'Kit guide';
  const tag = form.getAttribute('data-email-tag') || '';
  const conversionName = form.getAttribute('data-conversion-name') || 'guide_request';

  form.addEventListener('submit', () => {
    const detail = { guide, tag, conversionName, provider: 'kit' };
    window.dispatchEvent(new CustomEvent('leadFormSubmit', { detail }));
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push({ event: 'lead_form_submit', guide, tag, conversion_name: conversionName, provider: 'kit' });
    }
  });
});

// Preview-safe lead forms.
// These remain only for lead magnets whose production Kit HTML has not been provided yet.
document.querySelectorAll('form[data-kit-placeholder]').forEach((form) => {
  const input = form.querySelector('input[type="email"]');
  const error = form.querySelector('.form-error');
  const message = form.querySelector('.form-message');
  const guide = form.getAttribute('data-kit-placeholder') || 'this guide';
  const tag = form.getAttribute('data-email-tag') || '';
  const conversionName = form.getAttribute('data-conversion-name') || 'guide_request';

  const setError = (text) => {
    if (error) error.textContent = text;
    if (input) input.setAttribute('aria-invalid', text ? 'true' : 'false');
  };

  input?.addEventListener('input', () => {
    if (!input.value.trim() || isValidEmail(input.value.trim())) setError('');
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const email = input?.value?.trim() || '';

    if (!email) {
      setError('Enter your email address to get the guide.');
      input?.focus();
      return;
    }

    if (!isValidEmail(email)) {
      setError('Enter a valid email address, like name@example.com.');
      input?.focus();
      return;
    }

    setError('');

    const detail = { guide, tag, conversionName };
    window.dispatchEvent(new CustomEvent('leadFormPreviewSubmit', { detail }));
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push({ event: 'lead_form_submit_preview', guide, tag, conversion_name: conversionName });
    }

    if (message) {
      message.textContent = `Success — this preview form validated your email for ${guide}. Connect the live email form before production collection.`;
      message.classList.add('is-visible');
    }
  });
});
