class MatomoTrackingHandler {
  static DEBUG_KEY = 'csplab-matomo-debug';

  /** @type {MutationObserver} */
  observer;

  constructor() {
    this.init();
  }

  init() {
    MatomoTrackingHandler.log('init');
    this.setupDeclarativeClickEvents();
    this.setupHTMXVirtualPageViews();
    this.fireAutoEvents();
    this.observer = new MutationObserver(() => this.fireAutoEvents());
    this.observer.observe(document.body, { childList: true, subtree: true });
  }

  /**
   * @param {string} category
   * @param {string} action
   * @param {string|null} name
   * @param {number|null} value
   */
  static trackEvent(category, action, name, value) {
    const paq = (window._paq ??= []);
    const args = ['trackEvent', category, action];
    if (name != null) args.push(String(name));
    if (value != null) args.push(Number(value));
    paq.push(args);
    MatomoTrackingHandler.log('trackEvent', { category, action, name, value });
    document.dispatchEvent(new CustomEvent('matomo:event', {
      detail: { category, action, name, value },
    }));
  }

  /**
   * @param {number} id
   * @param {string} value
   */
  static setCustomDimension(id, value) {
    const paq = (window._paq ??= []);
    paq.push(['setCustomDimension', id, value]);
    MatomoTrackingHandler.log('setCustomDimension', { id, value });
  }

  setupDeclarativeClickEvents() {
    document.addEventListener('click', (e) => this.handleDeclarativeClick(e));
  }

  /**
   * @param {MouseEvent} e
   */
  handleDeclarativeClick(e) {
    const el = e.target.closest('[data-matomo-event]');
    if (!el) return;
    const [category, action, name, value] = el.dataset.matomoEvent.split('|');
    MatomoTrackingHandler.trackEvent(category, action, name, value);
  }

  fireAutoEvents() {
    for (const el of document.querySelectorAll('[data-matomo-autofire]')) {
      const [category, action, name, value] = el.dataset.matomoAutofire.split('|');
      MatomoTrackingHandler.trackEvent(category, action, name, value);
      el.removeAttribute('data-matomo-autofire');
    }
  }

  setupHTMXVirtualPageViews() {
    document.addEventListener('htmx:pushedIntoHistory', (e) => this.handleHistoryPush(e));
  }

  /**
   * @param {CustomEvent} e
   */
  handleHistoryPush(e) {
    const paq = (window._paq ??= []);
    paq.push(['setCustomUrl', e.detail.path]);
    paq.push(['setDocumentTitle', document.title]);
    paq.push(['trackPageView']);
    MatomoTrackingHandler.log('virtualPageView', { path: e.detail.path, title: document.title });
  }

  /**
   * @returns {boolean}
   */
  static isDebug() {
    return localStorage.getItem(MatomoTrackingHandler.DEBUG_KEY) === 'true';
  }

  /**
   * @param  {...any} args
   */
  static log(...args) {
    if (MatomoTrackingHandler.isDebug()) {
      console.debug('%c[matomo]', 'color: #e77000; font-weight: bold', ...args);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new MatomoTrackingHandler();
});
window.csplab = window.csplab || {};
window.csplab.matomo = MatomoTrackingHandler;
