from flask import Flask, request, jsonify, render_template, render_template_string, redirect, url_for
import json
from flask import send_from_directory
from google_utils import scrivi_su_google_sheet
from google_utils import scrivi_evento_ufficiale, leggi_eventi_ufficiali
from functools import wraps
from dotenv import load_dotenv
from flask import Response

from flask_cors import CORS
import os
from datetime import datetime

def check_auth(username, password):
    return username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD")

def authenticate():
    return Response(
        "Autenticazione richiesta", 401,
        {"WWW-Authenticate": 'Basic realm="Login richiesto"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


load_dotenv()


app = Flask(__name__)
CORS(app)

# ✅ Homepage base di test


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/oggi.html')
def pagina_oggi():
    return render_template("oggi.html")

@app.route('/index.html')
def pagina_index():
    return render_template("index.html")



@app.route('/api/events')
def get_events():
    try:
        giorno = int(request.args.get("giorno"))
        mese = int(request.args.get("mese"))
    except:
        return jsonify({"errore": "Parametri non validi"}), 400

    oggi = datetime.now()

    try:
        # Lettura eventi dal Google Sheet
        SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        RANGE = "Foglio1!A1:G"
        CHIAVE_JSON = "google-credentials.json"
        eventi = leggi_eventi_ufficiali(SHEET_ID, RANGE, CHIAVE_JSON)
    except Exception as e:
        print("❌ Errore lettura da Google Sheets:", e)
        return jsonify([]), 500

    # Filtra per giorno e mese
    filtrati = []
    for e in eventi:
        if e["giorno"] == giorno and e["mese"] == mese:
            anni_trascorsi = oggi.year - e["anno"]
            e["anni_fa"] = anni_trascorsi
            filtrati.append(e)

    return jsonify(filtrati)


@app.route('/')
def home_redirect():
    return redirect('/oggi.html')

@app.route('/proponi.html')
def pagina_proponi():
    return render_template("proponi.html")



@app.route('/api/proponi', methods=['POST'])
def proponi_evento():
    proposta = {
        "titolo": request.form["titolo"],
        "descrizione": request.form["descrizione"],
        "anno": request.form["anno"],
        "giorno": request.form["giorno"],
        "mese": request.form["mese"],
        "link": request.form.get("link", ""),
        "immagine_url": request.form.get("immagine_url", "")
    }

    # Parametri: ID foglio, range e percorso credenziali
    SHEET_ID = "10qFQ7SfBvbtm01NDFMRyP-fx9gcalu2Xx0HBITV1MsI"
    RANGE = "Foglio1!A1"
    CHIAVE_JSON = "google-credentials.json"

    try:
        scrivi_su_google_sheet(proposta, SHEET_ID, RANGE, CHIAVE_JSON)
        print("✅ Proposta salvata su Google Sheets")
    except Exception as e:
        print("❌ Errore durante salvataggio su Google Sheets:", e)

    return render_template("grazie.html")


@app.route('/admin')
@requires_auth
def pagina_admin():
    return render_template("admin.html")

@app.route('/api/admin/aggiungi', methods=['POST'])
@requires_auth
def aggiungi_evento_ufficiale():
    evento = {
        "giorno": int(request.form["giorno"]),
        "mese": int(request.form["mese"]),
        "anno": int(request.form["anno"]),
        "titolo": request.form["titolo"],
        "descrizione": request.form["descrizione"],
        "link": request.form.get("link", ""),
        "immagine_url": request.form.get("immagine_url", "")
    }

    try:
        SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        RANGE = "Foglio1!A1"
        CHIAVE_JSON = "google-credentials.json"
        scrivi_evento_ufficiale(evento, SHEET_ID, RANGE, CHIAVE_JSON)
        print("✅ Evento ufficiale salvato su Google Sheets")
    except Exception as e:
        print("❌ Errore salvataggio evento ufficiale:", e)
        return "Errore salvataggio", 500

    return redirect("/admin")

@app.route('/eventi.json')
def eventi_ufficiali_json():
    try:
        SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        RANGE = "Foglio1!A1:G"
        CHIAVE_JSON = "google-credentials.json"
        eventi = leggi_eventi_ufficiali(SHEET_ID, RANGE, CHIAVE_JSON)
        return jsonify(eventi)
    except Exception as e:
        print("❌ Errore lettura eventi:", e)
        return jsonify([]), 500




