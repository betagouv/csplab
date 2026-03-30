class CandidateTrackingHandler {
  static DRAWER_BODY_ID = 'opportunity-drawer-body';
  static PROCESSING_START_KEY = 'csplab-matomo-processing-start';

  /** @type {string|null} */
  lastDrawerOpportunity;

  constructor() {
    this.lastDrawerOpportunity = null;
    this.setupProcessingDuration();
  }

  init() {
    this.setupDrawerTracking();
  }

  setupProcessingDuration() {
    document.addEventListener('matomo:event', (e) => this.handleTrackingEvent(e));
  }

  /**
   * @param {CustomEvent} e
   */
  handleTrackingEvent(e) {
    const { category, action } = e.detail;

    if (category === 'CVProcessing' && action === 'started') {
      sessionStorage.setItem(CandidateTrackingHandler.PROCESSING_START_KEY, String(Date.now()));
      return;
    }

    if (category === 'CVResults' && (action === 'displayed' || action === 'no_results')) {
      const start = sessionStorage.getItem(CandidateTrackingHandler.PROCESSING_START_KEY);
      if (start) {
        const durationSeconds = Math.round((Date.now() - Number(start)) / 1000);
        window.csplab.matomo.trackEvent('CVProcessing', 'duration', action, durationSeconds);
        sessionStorage.removeItem(CandidateTrackingHandler.PROCESSING_START_KEY);
      }
    }
  }

  setupDrawerTracking() {
    document.addEventListener('htmx:afterSwap', (e) => this.handleDrawerSwap(e));
    const drawer = document.getElementById(CandidateTrackingHandler.DRAWER_BODY_ID)?.closest('dialog');
    if (drawer) {
      drawer.addEventListener('close', () => this.handleDrawerClose());
    }
  }

  /**
   * @param {CustomEvent} e
   */
  handleDrawerSwap(e) {
    if (e.detail.target?.id !== CandidateTrackingHandler.DRAWER_BODY_ID) return;
    const feedback = e.detail.target.querySelector('[data-opportunity-type][data-opportunity-id]');
    if (!feedback) return;
    const name = `${feedback.dataset.opportunityType}:${feedback.dataset.opportunityId}`;
    this.lastDrawerOpportunity = name;
    window.csplab.matomo.trackEvent('OpportunityDrawer', 'opened', name);
  }

  handleDrawerClose() {
    window.csplab.matomo.trackEvent('OpportunityDrawer', 'closed', this.lastDrawerOpportunity);
    this.lastDrawerOpportunity = null;
  }
}

const candidateTracking = new CandidateTrackingHandler();

document.addEventListener('DOMContentLoaded', () => {
  candidateTracking.init();
});
