class OpportunityFeedbackHandler {
  static STORAGE_KEY = 'csplab-feedback';
  static DEBUG_KEY = 'csplab-feedback-debug';
  static THROTTLE_MS = 1000;
  static ICON_RE = /fr-icon-thumb-(up|down)-(line|fill)/;

  /** @type {HTMLElement} */
  container;

  /** @type {string} */
  opportunityId;

  /** @type {string} */
  opportunityType;

  /** @type {number|null} */
  throttleTimer;

  /**
   * @param {HTMLElement} container
   */
  constructor(container) {
    this.container = container;
    this.opportunityId = container.dataset.opportunityId;
    this.opportunityType = container.dataset.opportunityType;
    this.throttleTimer = null;

    this.init();
  }

  init() {
    this.restoreState();
    OpportunityFeedbackHandler.log('init', {
      opportunityId: this.opportunityId,
      opportunityType: this.opportunityType,
      restored: OpportunityFeedbackHandler.getStoredFeedbacks()[this.opportunityId] ?? null,
    });

    if (this.container.dataset.feedbackInit) return;
    this.container.dataset.feedbackInit = 'true';

    this.setupClickHandler();
  }

  restoreState() {
    const stored = OpportunityFeedbackHandler.getStoredFeedbacks();
    if (stored[this.opportunityId]) {
      this.updateButtonStates(stored[this.opportunityId]);
    }
  }

  setupClickHandler() {
    this.container.addEventListener('click', (e) => this.handleClick(e));
  }

  /**
   * @param {MouseEvent} e
   */
  handleClick(e) {
    const btn = e.target.closest('.csplab-feedback__btn');
    if (!btn) return;
    if (this.throttleTimer) return;

    const { sentiment } = btn.dataset;

    this.throttleTimer = setTimeout(() => {
      this.setThrottled(false);
      this.throttleTimer = null;
    }, OpportunityFeedbackHandler.THROTTLE_MS);
    this.setThrottled(true);

    const currentSentiment = OpportunityFeedbackHandler.getStoredFeedbacks()[this.opportunityId];

    if (currentSentiment === sentiment) {
      this.updateButtonStates(null);
      OpportunityFeedbackHandler.removeFeedback(this.opportunityId);
      this.trackMatomoEvent('neutral');
      return;
    }

    this.updateButtonStates(sentiment);
    OpportunityFeedbackHandler.storeFeedback(this.opportunityId, sentiment);
    this.trackMatomoEvent(sentiment);
  }

  /**
   * @param {string|null} activeSentiment
   */
  updateButtonStates(activeSentiment) {
    for (const btn of this.container.querySelectorAll('.csplab-feedback__btn')) {
      const isActive = btn.dataset.sentiment === activeSentiment;
      btn.setAttribute('aria-pressed', String(isActive));

      const match = btn.className.match(OpportunityFeedbackHandler.ICON_RE);
      if (match) {
        const variant = isActive ? 'fill' : 'line';
        btn.className = btn.className.replace(
          OpportunityFeedbackHandler.ICON_RE,
          `fr-icon-thumb-${match[1]}-${variant}`,
        );
      }
    }
  }

  /**
   * @param {boolean} throttled
   */
  setThrottled(throttled) {
    this.container.classList.toggle('csplab-feedback--throttled', throttled);
  }

  /**
   * @param {string} sentiment
   */
  trackMatomoEvent(sentiment) {
    const label = `${this.opportunityType}:${this.opportunityId}`;
    OpportunityFeedbackHandler.log('trackEvent', {
      category: 'OpportunityFeedback',
      action: sentiment,
      name: label,
    });

    const paq = (window._paq ??= []);
    paq.push(['trackEvent', 'OpportunityFeedback', sentiment, label]);
  }

  /**
   * @returns {boolean}
   */
  static isDebug() {
    return localStorage.getItem(OpportunityFeedbackHandler.DEBUG_KEY) === 'true';
  }

  /**
   * @param  {...any} args
   */
  static log(...args) {
    if (OpportunityFeedbackHandler.isDebug()) {
      console.debug('%c[feedback]', 'color: #6a6af4; font-weight: bold', ...args);
    }
  }

  /**
   * @returns {Record<string, string>}
   */
  static getStoredFeedbacks() {
    try {
      return JSON.parse(localStorage.getItem(OpportunityFeedbackHandler.STORAGE_KEY) ?? '{}');
    } catch {
      return {};
    }
  }

  /**
   * @param {string} opportunityId
   * @param {string} sentiment
   */
  static storeFeedback(opportunityId, sentiment) {
    const feedbacks = OpportunityFeedbackHandler.getStoredFeedbacks();
    feedbacks[opportunityId] = sentiment;
    localStorage.setItem(OpportunityFeedbackHandler.STORAGE_KEY, JSON.stringify(feedbacks));
  }

  /**
   * @param {string} opportunityId
   */
  static removeFeedback(opportunityId) {
    const feedbacks = OpportunityFeedbackHandler.getStoredFeedbacks();
    delete feedbacks[opportunityId];
    localStorage.setItem(OpportunityFeedbackHandler.STORAGE_KEY, JSON.stringify(feedbacks));
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.csplab-feedback').forEach((el) => new OpportunityFeedbackHandler(el));
});

document.addEventListener('htmx:afterSwap', () => {
  document.querySelectorAll('.csplab-feedback').forEach((el) => new OpportunityFeedbackHandler(el));
});
