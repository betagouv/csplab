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
    this.markTriggers();
    this.setupHtmxListeners();
    this.setupClose();
    this.setupFocusRestore();
  }

  markTriggers() {
    const targetId = this.body.id;
    if (!targetId) return;
    document.querySelectorAll('[data-drawer-open]').forEach((el) => {
      el.setAttribute('hx-get', el.getAttribute('href'));
      el.setAttribute('hx-target', `#${targetId}`);
      el.setAttribute('hx-swap', 'innerHTML');
      el.setAttribute('aria-haspopup', 'dialog');
      htmx.process(el);
    });
  }

  setupHtmxListeners() {
    document.body.addEventListener('htmx:beforeRequest', (e) => this.handleBeforeRequest(e));
    document.body.addEventListener('htmx:afterSwap', (e) => this.handleAfterSwap(e));
    document.body.addEventListener('htmx:afterSettle', (e) => this.handleAfterSettle(e));
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

  /**
   * @param {CustomEvent} e
   */
  handleAfterSettle(e) {
    if (e.detail?.target === this.body) return;
    this.markTriggers();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-drawer]').forEach((dialog) => {
    if (typeof dialog.showModal === 'function') {
      new DrawerHandler(dialog);
    }
  });
});
