Uruchomienie projektu (windows powershell, przetestowane i powinno działać):

python -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=app.py
flask run


Uruchomienie projektu (linux):

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run


