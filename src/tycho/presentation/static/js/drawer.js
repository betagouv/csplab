class DrawerHandler {
  static DRAWER_SELECTOR = '[data-drawer]';
  static TRIGGER_SELECTOR = '[data-drawer-open]';
  static CLOSE_SELECTOR = '[data-drawer-close]';
  static HISTORY_MARKER = 'csplabDrawerOpen';

  /** @type {HTMLElement|null} */
  lastTrigger;

  constructor() {
    this.lastTrigger = null;
  }

  init() {
    this.markTriggers(document);
    document.body.addEventListener('htmx:beforeRequest', (e) => this.handleBeforeRequest(e));
    document.body.addEventListener('htmx:afterSwap', (e) => this.handleAfterSwap(e));
    window.addEventListener('popstate', () => this.closeOpenDrawer());
    window.addEventListener('pageshow', (e) => {
      if (e.persisted) this.closeOpenDrawer();
    });
  }

  /**
   * @param {ParentNode} root
   */
  markTriggers(root) {
    const scope = root && root.querySelectorAll ? root : document;
    scope.querySelectorAll(DrawerHandler.TRIGGER_SELECTOR).forEach((el) => {
      if (el.hasAttribute('hx-get')) return;
      const href = el.getAttribute('href');
      if (!href) return;
      el.setAttribute('hx-get', href);
      el.setAttribute('hx-target', 'body');
      el.setAttribute('hx-swap', 'beforeend');
      el.setAttribute('aria-haspopup', 'dialog');
      if (window.htmx) window.htmx.process(el);
    });
  }

  /**
   * @param {CustomEvent} e
   */
  handleBeforeRequest(e) {
    const trigger = e.detail?.elt;
    if (trigger?.matches?.(DrawerHandler.TRIGGER_SELECTOR)) {
      this.lastTrigger = trigger;
    }
  }

  /**
   * @param {CustomEvent} e
   */
  handleAfterSwap(e) {
    const trigger = e.detail?.requestConfig?.elt;
    if (!trigger?.matches?.(DrawerHandler.TRIGGER_SELECTOR)) {
      this.markTriggers(e.detail?.target);
      return;
    }
    const dialogs = document.querySelectorAll(DrawerHandler.DRAWER_SELECTOR);
    const dialog = dialogs[dialogs.length - 1];
    if (dialog) this.activateDrawer(dialog);
  }

  /**
   * @param {HTMLDialogElement} dialog
   */
  activateDrawer(dialog) {
    if (typeof dialog.showModal !== 'function') return;

    dialog.showModal();

    if (!history.state?.[DrawerHandler.HISTORY_MARKER]) {
      history.pushState({ [DrawerHandler.HISTORY_MARKER]: true }, '', window.location.href);
    }

    requestAnimationFrame(() => {
      const closeBtn = dialog.querySelector(DrawerHandler.CLOSE_SELECTOR);
      if (closeBtn) closeBtn.focus();
    });

    dialog.addEventListener('click', (e) => {
      if (e.target === dialog || e.target.closest?.(DrawerHandler.CLOSE_SELECTOR)) {
        dialog.close();
      }
    });

    dialog.addEventListener('close', () => this.handleDialogClose(dialog));
  }

  /**
   * @param {HTMLDialogElement} dialog
   */
  handleDialogClose(dialog) {
    if (history.state?.[DrawerHandler.HISTORY_MARKER]) {
      history.back();
    }
    dialog.remove();
    if (typeof this.lastTrigger?.focus === 'function') {
      this.lastTrigger.focus();
    }
    this.lastTrigger = null;
  }

  closeOpenDrawer() {
    const dialog = document.querySelector(`${DrawerHandler.DRAWER_SELECTOR}[open]`);
    if (!dialog) return;
    if (history.state?.[DrawerHandler.HISTORY_MARKER]) {
      history.replaceState(null, '', window.location.href);
    }
    dialog.close();
  }
}

const drawerHandler = new DrawerHandler();

document.addEventListener('DOMContentLoaded', () => {
  drawerHandler.init();
});
