/* ══════════════════════════════════════════════════════════════════════
   StudyMoo — Main JavaScript
   Handles: mobile nav, file drop zone, progress bar, message dismiss
   ══════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Mobile Nav Toggle ─────────────────────────────────────────────
  const navToggle   = document.getElementById('navToggle');
  const mobileSearch = document.getElementById('mobileSearch');

  if (navToggle && mobileSearch) {
    navToggle.addEventListener('click', function () {
      mobileSearch.classList.toggle('open');
    });
  }

  // ── Auto-dismiss Flash Messages ───────────────────────────────────
  const msgs = document.querySelectorAll('[data-auto-dismiss]');
  msgs.forEach(function (msg) {
    setTimeout(function () {
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(20px)';
      msg.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      setTimeout(function () { msg.remove(); }, 400);
    }, 5000);
  });

  // ── File Upload Drop Zone ─────────────────────────────────────────
  const dropZone    = document.getElementById('dropZone');
  const fileInput   = document.getElementById('id_file_upload');
  const dropPreview = document.getElementById('dropPreview');
  const dropInner   = dropZone ? dropZone.querySelector('.drop-inner') : null;
  const dropFileName = document.getElementById('dropFileName');
  const dropFileSize = document.getElementById('dropFileSize');
  const dropFileIcon = document.getElementById('dropFileIcon');

  if (dropZone && fileInput) {

    // Click drop zone to trigger file input
    dropZone.addEventListener('click', function (e) {
      if (!e.target.closest('input')) {
        fileInput.click();
      }
    });

    // File type icons
    const extIcons = {
      pdf: '📄', doc: '📝', docx: '📝',
      ppt: '📊', pptx: '📊', xls: '📈', xlsx: '📈',
      txt: '📃', zip: '🗜️', png: '🖼️', jpg: '🖼️', jpeg: '🖼️'
    };

    function formatBytes(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }

    function showFilePreview(file) {
      const ext = file.name.split('.').pop().toLowerCase();
      if (dropInner)   dropInner.style.display = 'none';
      if (dropPreview) dropPreview.style.display = 'flex';
      if (dropFileIcon) dropFileIcon.textContent = extIcons[ext] || '📁';
      if (dropFileName) dropFileName.textContent = file.name;
      if (dropFileSize) dropFileSize.textContent = formatBytes(file.size);
      dropZone.style.borderColor = 'var(--primary)';
      dropZone.style.background  = 'rgba(34,87,122,.04)';
    }

    fileInput.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        showFilePreview(this.files[0]);
      }
    });

    // Drag and drop
    dropZone.addEventListener('dragover', function (e) {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', function (e) {
      if (!dropZone.contains(e.relatedTarget)) {
        dropZone.classList.remove('drag-over');
      }
    });

    dropZone.addEventListener('drop', function (e) {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      const files = e.dataTransfer.files;
      if (files && files[0]) {
        // Transfer to file input via DataTransfer
        try {
          const dt = new DataTransfer();
          dt.items.add(files[0]);
          fileInput.files = dt.files;
        } catch (err) {
          // Fallback: show preview only (some browsers restrict this)
        }
        showFilePreview(files[0]);
      }
    });
  }

  // ── Upload Progress Indicator ──────────────────────────────────────
  const uploadForm   = document.getElementById('uploadForm');
  const progressWrap = document.getElementById('uploadProgress');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  const submitBtn    = document.getElementById('submitBtn');

  if (uploadForm && progressWrap && progressFill) {
    uploadForm.addEventListener('submit', function () {
      // Show progress bar
      progressWrap.style.display = 'block';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading…';
      }

      // Fake smooth progress animation
      let pct = 0;
      const interval = setInterval(function () {
        pct += Math.random() * 15;
        if (pct > 90) pct = 90;
        progressFill.style.width = pct + '%';
        if (progressText) progressText.textContent = 'Uploading… ' + Math.round(pct) + '%';
      }, 300);

      // Cleanup on page unload
      window.addEventListener('beforeunload', function () {
        clearInterval(interval);
      });
    });
  }

  // ── Card hover ripple effect ───────────────────────────────────────
  document.querySelectorAll('.resource-card').forEach(function (card) {
    card.addEventListener('mouseenter', function () {
      card.style.willChange = 'transform';
    });
    card.addEventListener('mouseleave', function () {
      card.style.willChange = 'auto';
    });
  });

  // ── Smooth scroll for anchor links ────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Search input — clear on Escape ────────────────────────────────
  const searchInputs = document.querySelectorAll('.search-input');
  searchInputs.forEach(function (input) {
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { this.value = ''; this.blur(); }
    });
  });

  // ── Filter selects auto-submit ─────────────────────────────────────
  // (handled inline with onchange in template — no extra JS needed)

});
