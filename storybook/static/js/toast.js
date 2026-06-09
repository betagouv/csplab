document.querySelectorAll('.csplab-toast .fr-btn--close').forEach((btn) => {
  btn.removeAttribute('onclick');
  btn.addEventListener('click', () => btn.closest('.csplab-toast').remove());
});
