import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils.pdf_parser import extract_text_from_pdf
from utils.ai_generator import generate_questions

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None

    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == "":
            error = "Valitse tiedosto."
            return render_template('index.html', error=error)

        filename = file.filename.lower()

        try:
            # PDF
            if filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)

            # Plain text
            elif filename.endswith('.txt'):
                data = file.read()
                if isinstance(data, bytes):
                    text = data.decode('utf-8', errors='replace')
                else:
                    text = data

            else:
                error = "Tiedostomuotoa ei tueta. Lataa .pdf tai .txt."
                return render_template('index.html', error=error)

            if not text or not text.strip():
                error = "Tiedosto on tyhjä tai tekstin poiminta epäonnistui."
                return render_template('index.html', error=error)

            # Generate questions
            questions = generate_questions(text)

            if not questions:
                error = "Kysymysten generointi epäonnistui. Katso palvelimen loki."
                return render_template('index.html', error=error)

            session['questions'] = questions
            return redirect(url_for('quiz'))

        except Exception as e:
            print("SERVER ERROR:", e)
            error = f"Virhe: {e}"
            return render_template('index.html', error=error)

    return render_template('index.html', error=error)

@app.route('/quiz')
def quiz():
    questions = session.get('questions', [])
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    questions = session.get('questions', [])
    score = 0

    for i, q in enumerate(questions, start=1):
        user_answer = request.form.get(f"q{i}")
        if user_answer and user_answer == q.get('correct_answer'):
            score += 1

    return f"<h2>Arvosanasi: {score}/{len(questions)}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
