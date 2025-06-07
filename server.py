from flask import Flask, request, jsonify, render_template, render_template_string, redirect, url_for
import json
from flask import send_from_directory
from google_utils import scrivi_su_google_sheet

from flask_cors import CORS
import os
from datetime import datetime

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
        with open("eventi.json", "r", encoding="utf-8") as f:
            eventi = json.load(f)
    except FileNotFoundError:
        eventi = []

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



