// Show loading indicator and prevent multiple submits
(function () {
    const form = document.getElementById('uploadForm');
    const loading = document.getElementById('loadingIndicator');
    const submitBtn = document.getElementById('submitBtn');

    if (!form || !loading || !submitBtn) return;

    form.addEventListener('submit', function () {
        // Disable submit button to avoid double submits and show spinner.
        submitBtn.disabled = true;
        loading.style.display = 'block';
        // Do not disable other inputs (they must be submitted).
    });
})();