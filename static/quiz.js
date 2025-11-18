// Client-side grading: näyttää per-kysymys palautteen ja kokonaispisteet.
// Tämä skripti estää lomakkeen normaalin lähetyksen ja toimii kokonaan selaimessa.
document.addEventListener('DOMContentLoaded', function () {
    // Hae tärkeät elementit DOM:sta
    const checkBtn = document.getElementById('checkBtn');
    const resetBtn = document.getElementById('resetBtn');
    const quizForm = document.getElementById('quizForm');
    const resultSummary = document.getElementById('resultSummary');

    // Jos ei ole quizFormia, lopetetaan (turvallisuustarkistus)
    if (!quizForm) return;

    // Estetään Enter-näppäimen tai muunkin submitin aiheuttama sivunvaihto
    quizForm.addEventListener('submit', function (e) {
        e.preventDefault();
    });

    // "Tarkista vastaukset" -toiminto
    if (checkBtn) {
        checkBtn.addEventListener('click', function () {
            // Hae kaikki kysymyslohkot ja laske pisteet
            const questionBlocks = Array.from(quizForm.querySelectorAll('.question-block'));
            let score = 0;
            let total = questionBlocks.length;

            questionBlocks.forEach((block, idx) => {
                const qIndex = idx + 1;
                // data-correct sisältää oikean vastauksen stringinä
                const correct = block.dataset.correct;
                const selectedInput = block.querySelector(`input[name="q${qIndex}"]:checked`);
                const feedbackEl = block.querySelector('.feedback');

                // Poistetaan aiemmat luokat/palautteet
                block.querySelectorAll('.option-label').forEach(lbl => {
                    lbl.classList.remove('correct', 'incorrect', 'correct-answer');
                });

                if (selectedInput) {
                    const selectedVal = selectedInput.value;
                    const selectedLabel = selectedInput.closest('label') || quizForm.querySelector(`label[for="${selectedInput.id}"]`);
                    if (selectedVal === correct) {
                        // Oikea vastaus
                        score += 1;
                        if (selectedLabel) selectedLabel.classList.add('correct');
                        feedbackEl.textContent = 'Oikein ✓';
                        feedbackEl.style.color = '#155724';
                    } else {
                        // Väärä vastaus: merkataan valittu ja korostetaan oikea
                        if (selectedLabel) selectedLabel.classList.add('incorrect');
                        feedbackEl.textContent = 'Väärin ✗';
                        feedbackEl.style.color = '#721c24';
                        const correctInput = block.querySelector(`input[type="radio"][value="${correct}"]`);
                        if (correctInput) {
                            const correctLabel = correctInput.closest('label') || quizForm.querySelector(`label[for="${correctInput.id}"]`);
                            if (correctLabel) correctLabel.classList.add('correct-answer');
                        }
                    }
                } else {
                    // Ei vastausta: kerrotaan käyttäjälle ja korostetaan oikea
                    feedbackEl.textContent = 'Ei vastausta';
                    feedbackEl.style.color = '#856404';
                    const correctInput = block.querySelector(`input[type="radio"][value="${correct}"]`);
                    if (correctInput) {
                        const correctLabel = correctInput.closest('label') || quizForm.querySelector(`label[for="${correctInput.id}"]`);
                        if (correctLabel) correctLabel.classList.add('correct-answer');
                    }
                }

                // Emme disabloi inputteja, jotta käyttäjä voi resetata tai muokata ennen uudelleentarkistusta
            });

            // Näytetään pistemäärä
            resultSummary.textContent = `Pistemäärä: ${score}/${total}`;
            // Estetään tarkistuspainikkeen uudelleenkäyttö ennen resettiä
            checkBtn.disabled = true;
        });
    }

    // "Tyhjennä vastaukset" -toiminto palauttaa alkuperäisen tilan
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            // Poista valinnat ja palauttele luokat/palautealueet
            quizForm.querySelectorAll('input[type="radio"]').forEach(i => {
                i.checked = false;
                i.disabled = false;
            });
            quizForm.querySelectorAll('.option-label').forEach(lbl => {
                lbl.classList.remove('correct', 'incorrect', 'correct-answer');
            });
            quizForm.querySelectorAll('.feedback').forEach(f => {
                f.textContent = '';
                f.style.color = '';
            });
            if (resultSummary) resultSummary.textContent = '';
            if (checkBtn) checkBtn.disabled = false;
        });
    }
});