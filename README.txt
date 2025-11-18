Kloonaa projekti PowerShellin kautta:
git clone https://github.com/diggeridoo95/tentinluoja

Luo juurihakemistoon .env -tiedosto ja lisää sen sisälle oma google AI:n API key, 
kirjoita .env:iin: 
GEMINI_API_KEY= tähän oma avaimesi 

API avaimen voit luoda osoitteessa "https://aistudio.google.com/app/api-keys" 
kirjautumalla sisään -> Create API key
(muista laittaa api key tilin ympäristömuuttujiin uutena muuttujana ja sen arvoksi itse avain)

Avaa projektikansio Vscodessa

Luo venv
VSC-Konsoliin:
python -m venv venv

Aktivoi venv
VSC-Konsoliin:

venv\Scripts\activate

(jos venv:in aktivointi antaa policy virheilmoituksen -> PowerShell: 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)

lataa vaadittavat kirjastot
VSC-Konsoliin:

pip install Flask python-dotenv google-generativeai PyMuPDF

VSC-Konsoliin:
python app.py 

avaa linkki: http://127.0.0.1:5000
pudota pdf ja luo tentti.
