import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils.pdf_parser import extract_text_from_pdf
from utils.ai_generator import generate_questions

# Sovellusolio ja salainen avain sessioita varten
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

# Päänäkymä: tiedoston lataus ja kysymysten generointi
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    GET: näyttää latauslomakkeen (templates/index.html).
    POST: vastaanottaa ladattavan tiedoston, poimii tekstin (PDF/TXT),
          lukee käyttäjän valitseman kysymysten määrän, kutsuu
          generate_questions ja tallentaa kysymykset sessioon.
    """
    error = None

    if request.method == 'POST':
        # Hae ladattu tiedosto lomakkeelta
        file = request.files.get('file')

        if not file or file.filename == "":
            error = "Valitse tiedosto."
            return render_template('index.html', error=error)

        filename = file.filename.lower()

        try:
            # Jos PDF -> käytä pdf_parseria
            if filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)

            # Jos plain text -> lue sisältöä
            elif filename.endswith('.txt'):
                data = file.read()
                # Flask file.read() palauttaa yleensä bytes, joten dekoodataan
                if isinstance(data, bytes):
                    text = data.decode('utf-8', errors='replace')
                else:
                    text = data

            else:
                # Muut tiedostotyypit eivät ole tuettuja
                error = "Tiedostomuotoa ei tueta. Lataa .pdf tai .txt."
                return render_template('index.html', error=error)

            # Varmista että teksti löytyy
            if not text or not text.strip():
                error = "Tiedosto on tyhjä tai tekstin poiminta epäonnistui."
                return render_template('index.html', error=error)

            # Lue ja validoi käyttäjän valitsema kysymysten määrä (5-20)
            num_q = request.form.get('num_questions', '5')
            try:
                num_q = int(num_q)
            except (ValueError, TypeError):
                num_q = 5
            num_q = max(5, min(20, num_q))

            # Kutsu tekoälygeneraattoria tuottamaan kysymykset
            questions = generate_questions(text, num_q)

            if not questions:
                error = "Kysymysten generointi epäonnistui. Katso palvelimen loki."
                return render_template('index.html', error=error)

            # Tallenna kysymykset sessioon jotta quiz-sivu voi lukea ne
            session['questions'] = questions
            return redirect(url_for('quiz'))

        except Exception as e:
            # Lokitetaan virhe ja näytetään käyttäjälle yksinkertainen viesti
            print("SERVER ERROR:", e)
            error = f"Virhe: {e}"
            return render_template('index.html', error=error)

    # GET -> näytä index
    return render_template('index.html', error=error)

# Quiz-sivu näyttää sessiossa olevat kysymykset
@app.route('/quiz')
def quiz():
    # Hae kysymykset sessiosta (tyhjä lista jos ei löydy)
    questions = session.get('questions', [])
    return render_template('quiz.html', questions=questions)

# Sovelluksen käynnistys
if __name__ == '__main__':
    app.run(debug=True)