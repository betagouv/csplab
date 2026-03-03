class DrawerHandler {
  /** @type {HTMLDialogElement} */
  dialog;

  /** @type {HTMLElement} */
  body;

  /** @type {HTMLElement|null} */
  triggerElement;

  /**
   * @param {HTMLDialogElement} dialog
   */
  constructor(dialog) {
    this.dialog = dialog;
    this.body = dialog.querySelector('[data-drawer-body]');
    this.triggerElement = null;

    if (!this.body) return;

    this.init();
  }

  init() {
    this.setupHtmxListeners();
    this.setupClose();
    this.setupFocusRestore();
  }

  setupHtmxListeners() {
    document.body.addEventListener('htmx:beforeRequest', (e) => this.handleBeforeRequest(e));
    document.body.addEventListener('htmx:afterSwap', (e) => this.handleAfterSwap(e));
  }

  setupClose() {
    this.dialog.addEventListener('click', (e) => this.handleClick(e));
  }

  setupFocusRestore() {
    this.dialog.addEventListener('close', () => this.handleClose());
  }

  /**
   * @param {CustomEvent} e
   */
  handleBeforeRequest(e) {
    if (e.detail?.target === this.body) {
      this.triggerElement = e.detail.elt || document.activeElement;
    }
  }

  /**
   * @param {CustomEvent} e
   */
  handleAfterSwap(e) {
    if (e.detail?.target !== this.body) return;

    const title = this.dialog.querySelector('[data-drawer-title]');
    if (title) {
      this.dialog.setAttribute('aria-labelledby', title.id);
      this.dialog.removeAttribute('aria-label');
    }

    if (!this.dialog.open) {
      this.dialog.showModal();
    }

    requestAnimationFrame(() => {
      const closeBtn = this.dialog.querySelector('[data-drawer-close]');
      if (closeBtn) closeBtn.focus();
    });
  }

  /**
   * @param {MouseEvent} e
   */
  handleClick(e) {
    if (e.target === this.dialog || e.target.closest('[data-drawer-close]')) {
      if (this.dialog.open) {
        this.dialog.close();
      }
    }
  }

  handleClose() {
    if (this.triggerElement && typeof this.triggerElement.focus === 'function') {
      this.triggerElement.focus();
    }
    this.triggerElement = null;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-drawer]').forEach((dialog) => {
    if (typeof dialog.showModal === 'function') {
      new DrawerHandler(dialog);
    }
  });
});
