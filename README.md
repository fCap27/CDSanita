
# ClinicaDemo - Progetto Healthcare Web App (Demo)

## Contenuto del progetto
- frontend/: HTML/CSS/JS semplice per gestire pazienti e appuntamenti
- backend/: Flask app con SQLite + API REST (CRUD)
- backend/swagger.json: semplice specifica OpenAPI
- Dockerfile nel backend per containerizzazione (opzionale)

## Esecuzione (locale)
1. Creare virtualenv e installare dipendenze
   $ python -m venv venv
   $ source venv/bin/activate
   $ pip install -r backend/requirements.txt
2. Avviare il backend
   $ cd backend
   $ python app.py
3. Aprire http://localhost:5000

## Note di progetto
- Ho scelto SQLite per semplicità (file-based). Per produzione usare PostgreSQL/MySQL.
- Dockerfile incluso per containerizzazione semplice.
