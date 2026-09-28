document.querySelectorAll('.csplab-notice .fr-btn--close').forEach((btn) => {
  btn.addEventListener('click', () => btn.closest('.csplab-notice').remove());
});
