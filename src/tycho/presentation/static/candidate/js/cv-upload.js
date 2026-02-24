class CVUploadHandler {
  /** @type {HTMLElement} */
  container;

  /** @type {HTMLElement|null} */
  dropzone;

  /** @type {HTMLInputElement|null} */
  fileInput;

  /** @type {HTMLElement|null} */
  fileCard;

  /** @type {HTMLElement|null} */
  fileName;

  /** @type {HTMLElement|null} */
  fileSize;

  /** @type {HTMLElement|null} */
  uploadActions;

  /** @type {HTMLButtonElement|null} */
  removeButton;

  /** @type {HTMLTemplateElement|null} */
  infoTemplate;

  /** @type {HTMLElement|null} */
  currentToast;

  /**
   * @param {HTMLElement} container
   */
  constructor(container) {
    this.container = container;
    this.dropzone = container.querySelector('[data-dropzone]');
    this.fileInput = container.querySelector('[data-file-input]');
    this.fileCard = container.querySelector('[data-file-card]');
    this.fileName = container.querySelector('[data-file-name]');
    this.fileSize = container.querySelector('[data-file-size]');
    this.uploadActions = container.querySelector('[data-upload-actions]');
    this.removeButton = container.querySelector('[data-remove-file]');
    this.infoTemplate = document.getElementById('info-toast-template');
    this.currentToast = null;

    this.init();
  }

  init() {
    if (!this.dropzone || !this.fileInput) return;

    this.preventNoJsFormValidationConflicts();
    this.setupDragAndDrop();
    this.setupFileInputChange();
    this.setupFileRemove();
  }

  preventNoJsFormValidationConflicts() {
    const noJsInput = this.container.querySelector('[data-nojs-input]');
    if (noJsInput) {
      noJsInput.disabled = true;
    }
  }

  setupDragAndDrop() {
    if (!this.dropzone) return;

    this.dropzone.addEventListener('dragover', (e) => this.handleDragOver(e));
    this.dropzone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    this.dropzone.addEventListener('drop', (e) => this.handleDrop(e));
  }

  setupFileInputChange() {
    if (!this.fileInput) return;

    this.fileInput.addEventListener('change', () => this.handleFileSelect());
  }

  setupFileRemove() {
    if (!this.removeButton) return;

    this.removeButton.addEventListener('click', () => this.handleRemove());
  }

  /**
   * @param {DragEvent} e
   */
  handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.dropzone.dataset.state = 'dragging';
  }

  /**
   * @param {DragEvent} e
   */
  handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.dropzone.dataset.state = 'initial';
  }

  /**
   * @param {DragEvent} e
   */
  handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    const file = e.dataTransfer?.files[0];
    if (file) {
      this.setFile(file);
    }
  }

  handleFileSelect() {
    const file = this.fileInput?.files?.[0];
    if (file) {
      this.hideToast();
      this.showFile(file);
    }
  }

  /**
   * @param {File} file
   */
  setFile(file) {
    this.hideToast();
    const dt = new DataTransfer();
    dt.items.add(file);
    if (this.fileInput) {
      this.fileInput.files = dt.files;
    }
    this.showFile(file);
  }

  /**
   * @param {File} file
   */
  showFile(file) {
    if (this.fileName) {
      this.fileName.textContent = file.name;
    }
    if (this.fileSize) {
      this.fileSize.textContent = this.formatSize(file.size);
    }
    if (this.dropzone) {
      this.dropzone.hidden = true;
    }
    if (this.fileCard) {
      this.fileCard.hidden = false;
    }
    if (this.uploadActions) {
      this.uploadActions.hidden = false;
      this.uploadActions.setAttribute('aria-hidden', 'false');
    }
  }

  /**
   * @param {number} bytes
   * @returns {string}
   */
  formatSize(bytes) {
    const KB = 1024;
    const MB = KB * 1024;

    if (bytes < KB) return `${bytes} octets`;
    if (bytes < MB) return `${(bytes / KB).toFixed(1)} Ko`;
    return `${(bytes / MB).toFixed(1)} Mo`;
  }

  hideToast() {
    if (this.currentToast) {
      this.currentToast.remove();
      this.currentToast = null;
    }
  }

  handleRemove() {
    if (this.fileInput) {
      this.fileInput.value = '';
    }

    if (this.fileCard) {
      this.fileCard.hidden = true;
    }
    if (this.dropzone) {
      this.dropzone.hidden = false;
      this.dropzone.dataset.state = 'initial';
    }
    if (this.uploadActions) {
      this.uploadActions.hidden = true;
      this.uploadActions.setAttribute('aria-hidden', 'true');
    }

    this.hideToast();
    this.showInfo();

    if (this.fileInput) {
      this.fileInput.focus();
    }
  }

  showInfo() {
    if (!this.infoTemplate) return;

    const toast = this.infoTemplate.content.cloneNode(true).firstElementChild;
    if (!toast) return;

    const closeBtn = toast.querySelector('.fr-btn--close');
    if (closeBtn) {
      closeBtn.removeAttribute('onclick');
      closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.hideToast();
      });
    }

    document.body.appendChild(toast);
    this.currentToast = toast;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const isTouchOnly = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  const form = document.getElementById('cv-upload-form');
  if (!form) return;

  if (isTouchOnly) {
    const noJsInput = form.querySelector('[data-nojs-input]');
    const noJsActions = form.querySelector('[data-nojs-actions]');
    if (noJsInput && noJsActions) {
      noJsInput.addEventListener('change', () => {
        noJsActions.hidden = !noJsInput.value;
      });
    }
    return;
  }

  new CVUploadHandler(form);
});
