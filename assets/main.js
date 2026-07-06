const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const initAnalytics = () => {
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {};
  window.plausible = window.plausible || function plausible() {};
};

const trackEvent = (eventName, props = {}) => {
  const payload = { event: eventName, ...props };
  if (Array.isArray(window.dataLayer)) {
    window.dataLayer.push(payload);
  }

  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, props);
  }

  if (typeof window.plausible === 'function') {
    window.plausible(eventName, { props });
  }
};

const ensureFormFeedback = (form, input, fieldName) => {
  let feedback = form.querySelector(`[data-error-for="${fieldName}"]`);
  if (!feedback) {
    feedback = document.createElement('p');
    feedback.className = 'form-error';
    feedback.setAttribute('data-error-for', fieldName);
    feedback.setAttribute('role', 'alert');
    feedback.setAttribute('aria-live', 'polite');
    input.parentElement?.insertBefore(feedback, input.nextSibling);
  }
  return feedback;
};

const ensureFormStatus = (form) => {
  let status = form.querySelector('.form-status');
  if (!status) {
    status = document.createElement('p');
    status.className = 'form-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    form.appendChild(status);
  }
  return status;
};

const setFieldError = (input, feedback, message) => {
  if (!input) return;
  input.setAttribute('aria-invalid', message ? 'true' : 'false');
  if (feedback) feedback.textContent = message || '';
};

const bindKitForm = (form) => {
  const guide = form.querySelector('input[name="form-name"]')?.value || 'Kit guide';
  const tag = form.getAttribute('data-email-tag') || '';
  const conversionName = form.getAttribute('data-conversion-name') || 'guide_request';
  const firstName = form.querySelector('input[name="fields[first_name]"]');
  const email = form.querySelector('input[name="email_address"]');
  const firstNameFeedback = firstName ? ensureFormFeedback(form, firstName, 'first_name') : null;
  const emailFeedback = email ? ensureFormFeedback(form, email, 'email_address') : null;
  const status = ensureFormStatus(form);

  if (!form.dataset.analyticsTracked) {
    form.dataset.analyticsTracked = 'true';
    trackEvent('lead_form_view', { guide, tag, conversion_name: conversionName, provider: 'kit' });
  }

  const clearErrors = () => {
    setFieldError(firstName, firstNameFeedback, '');
    setFieldError(email, emailFeedback, '');
    status.textContent = '';
    status.classList.remove('is-visible');
  };

  firstName?.addEventListener('input', () => {
    if (firstName.value.trim()) {
      setFieldError(firstName, firstNameFeedback, '');
    }
  });

  email?.addEventListener('input', () => {
    if (!email.value.trim() || isValidEmail(email.value.trim())) {
      setFieldError(email, emailFeedback, '');
    }
  });

  form.addEventListener('submit', (event) => {
    trackEvent('lead_form_submit_attempt', { guide, tag, conversion_name: conversionName, provider: 'kit' });

    const firstNameValue = firstName?.value?.trim() || '';
    const emailValue = email?.value?.trim() || '';
    let hasError = false;

    clearErrors();

    if (!firstNameValue) {
      setFieldError(firstName, firstNameFeedback, 'Please enter your first name.');
      hasError = true;
    }

    if (!emailValue) {
      setFieldError(email, emailFeedback, 'Please enter your email address.');
      hasError = true;
    } else if (!isValidEmail(emailValue)) {
      setFieldError(email, emailFeedback, 'Please enter a valid email address.');
      hasError = true;
    }

    if (hasError) {
      event.preventDefault();
      status.textContent = 'Please fix the highlighted fields and try again.';
      status.classList.add('is-visible');
      return;
    }

    const detail = { guide, tag, conversionName, provider: 'kit' };
    window.dispatchEvent(new CustomEvent('leadFormSubmit', { detail }));
    trackEvent('lead_form_submit_success', { guide, tag, conversion_name: conversionName, provider: 'kit' });
    status.textContent = 'Thanks! Your guide request is being submitted.';
    status.classList.add('is-visible');
  });
};

document.querySelectorAll('form.kit-live-form').forEach(bindKitForm);

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
    trackEvent('lead_form_submit_attempt', { guide, tag, conversion_name: conversionName, provider: 'preview' });
    trackEvent('lead_form_submit_success', { guide, tag, conversion_name: conversionName, provider: 'preview' });

    if (message) {
      message.textContent = `Success — this preview form validated your email for ${guide}. Connect the live email form before production collection.`;
      message.classList.add('is-visible');
    }
  });
});

initAnalytics();

const linkEventMap = [
  { pattern: '/why-you-react-that-way/', eventName: 'individual_guide_click' },
  { pattern: '/why-you-keep-having-the-same-fight/', eventName: 'couples_guide_click' },
  { pattern: '/individual-coaching/', eventName: 'coaching_cta_click' },
  { pattern: '/couples-coaching/', eventName: 'coaching_cta_click' },
  { pattern: '/work-with-robert/', eventName: 'work_with_robert_click' }
];

document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link) return;

  const href = link.getAttribute('href') || '';
  const normalized = href.split('#')[0];
  const match = linkEventMap.find((entry) => normalized === entry.pattern);

  if (match) {
    trackEvent(match.eventName, { href: normalized });
  }
});
