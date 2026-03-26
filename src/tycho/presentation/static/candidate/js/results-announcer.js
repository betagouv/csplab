class ResultsAnnouncer {
  /** @type {HTMLElement} */
  resultsZone;

  /** @type {HTMLElement} */
  liveRegion;

  /**
   * @param {HTMLElement} resultsZone
   * @param {HTMLElement} liveRegion
   */
  constructor(resultsZone, liveRegion) {
    this.resultsZone = resultsZone;
    this.liveRegion = liveRegion;

    this.setupListeners();
  }

  setupListeners() {
    document.body.addEventListener('htmx:beforeRequest', (e) => {
      if (this.isResultsSwap(e)) {
        this.resultsZone.setAttribute('aria-busy', 'true');
      }
    });

    document.body.addEventListener('htmx:afterSettle', (e) => {
      if (this.isResultsSwap(e)) {
        this.clearBusy();
        this.announce();
      }
    });

    document.body.addEventListener('htmx:responseError', (e) => {
      if (this.isResultsSwap(e)) this.clearBusy();
    });

    document.body.addEventListener('htmx:sendError', (e) => {
      if (this.isResultsSwap(e)) this.clearBusy();
    });
  }

  clearBusy() {
    this.resultsZone.removeAttribute('aria-busy');
  }

  /** @param {CustomEvent} e */
  isResultsSwap(e) {
    return e.detail?.target === this.resultsZone;
  }

  announce() {
    const heading = this.resultsZone.querySelector('h2');
    if (!heading) return;

    this.liveRegion.textContent = '';
    setTimeout(() => {
      this.liveRegion.textContent = heading.textContent.trim();
    }, 100);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const resultsZone = document.getElementById('results-zone');
  const liveRegion = document.getElementById('results-live-region');
  if (resultsZone && liveRegion) {
    new ResultsAnnouncer(resultsZone, liveRegion);
  }
});
