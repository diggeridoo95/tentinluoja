// Client-side grading: shows per-question feedback and total score.
// Keeps server submission button intact.
document.addEventListener('DOMContentLoaded', function () {
    const checkBtn = document.getElementById('checkBtn');
    const resetBtn = document.getElementById('resetBtn');
    const quizForm = document.getElementById('quizForm');
    const resultSummary = document.getElementById('resultSummary');

    if (!quizForm) return;

    // Prevent normal form submit/navigation (e.g. Enter key)
    quizForm.addEventListener('submit', function (e) {
        e.preventDefault();
    });

    if (checkBtn) {
        checkBtn.addEventListener('click', function () {
            const questionBlocks = Array.from(quizForm.querySelectorAll('.question-block'));
            let score = 0;
            let total = questionBlocks.length;

            questionBlocks.forEach((block, idx) => {
                const qIndex = idx + 1;
                const correct = block.dataset.correct;
                const selectedInput = block.querySelector(`input[name="q${qIndex}"]:checked`);
                const feedbackEl = block.querySelector('.feedback');

                // Clear previous states
                block.querySelectorAll('.option-label').forEach(lbl => {
                    lbl.classList.remove('correct', 'incorrect', 'correct-answer');
                });

                if (selectedInput) {
                    const selectedVal = selectedInput.value;
                    const selectedLabel = selectedInput.closest('label') || quizForm.querySelector(`label[for="${selectedInput.id}"]`);
                    if (selectedVal === correct) {
                        // Correct
                        score += 1;
                        if (selectedLabel) selectedLabel.classList.add('correct');
                        feedbackEl.textContent = 'Oikein ✓';
                        feedbackEl.style.color = '#155724';
                    } else {
                        // Incorrect - mark selected and reveal correct
                        if (selectedLabel) selectedLabel.classList.add('incorrect');
                        feedbackEl.textContent = 'Väärin ✗';
                        feedbackEl.style.color = '#721c24';
                        // highlight correct option
                        const correctInput = block.querySelector(`input[type="radio"][value="${correct}"]`);
                        if (correctInput) {
                            const correctLabel = correctInput.closest('label') || quizForm.querySelector(`label[for="${correctInput.id}"]`);
                            if (correctLabel) correctLabel.classList.add('correct-answer');
                        }
                    }
                } else {
                    // No answer selected: reveal correct
                    feedbackEl.textContent = 'Ei vastausta';
                    feedbackEl.style.color = '#856404';
                    const correctInput = block.querySelector(`input[type="radio"][value="${correct}"]`);
                    if (correctInput) {
                        const correctLabel = correctInput.closest('label') || quizForm.querySelector(`label[for="${correctInput.id}"]`);
                        if (correctLabel) correctLabel.classList.add('correct-answer');
                    }
                }

                // Do NOT disable inputs here so user can reset if needed
            });

            resultSummary.textContent = `Pistemäärä: ${score}/${total}`;
            // disable check button after checking to avoid confusion
            checkBtn.disabled = true;
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            // Clear selections and feedback, restore button state
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