Uruchomienie projektu:

Stworzenie virualenv i instalacja wymaganych bibliotek pythonowych:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Uruchomienie frontendu:

cd frontend
npm install
npm start

Uruchomienie backendu:

cd backend
export FLASK_APP=app.py
flask run


