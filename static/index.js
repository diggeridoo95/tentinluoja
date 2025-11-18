// Näyttää lataus-spinnerin kun käyttäjä lähettää tiedoston index-lomakkeelta.
(function () {
    const form = document.getElementById('uploadForm');
    const loading = document.getElementById('loadingIndicator');
    const submitBtn = document.getElementById('submitBtn');

    // Jos elementtejä ei löydy, poistutaan (turvallisuus)
    if (!form || !loading || !submitBtn) return;

    // Kun lomake lähetetään, näytetään spinner ja estetään moninkertainen klikitys
    form.addEventListener('submit', function () {
        submitBtn.disabled = true;
        loading.style.display = 'block';
        // Muut kentät jätetään aktiivisiksi jotta ne tulevat mukaan post-pyyntöön
    });
})();