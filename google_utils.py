from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

def scrivi_su_google_sheet(dati, spreadsheet_id, range_destinazione, path_chiave_json):
    # Autenticazione con Service Account
    credentials = service_account.Credentials.from_service_account_file(
        path_chiave_json,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    # Valori da scrivere
    valori = [[
        dati.get("titolo", ""),
        dati.get("descrizione", ""),
        dati.get("anno", ""),
        dati.get("giorno", ""),
        dati.get("mese", ""),
        dati.get("link", ""),
        dati.get("immagine_url", "")
    ]]

    # Scrittura sul foglio
    body = {"values": valori}
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=range_destinazione,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    return result

# Per accesso da Service Account
def get_service_account_credentials(path_chiave_json):
    return service_account.Credentials.from_service_account_file(
        path_chiave_json,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

# ✅ Scrive un evento ufficiale nel Google Sheet principale
def scrivi_evento_ufficiale(evento, spreadsheet_id, range_destinazione, path_chiave_json):
    credentials = get_service_account_credentials(path_chiave_json)
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    valori = [[
        evento.get("giorno", ""),
        evento.get("mese", ""),
        evento.get("anno", ""),
        evento.get("titolo", ""),
        evento.get("descrizione", ""),
        evento.get("link", ""),
        evento.get("immagine_url", "")
    ]]

    body = {"values": valori}
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=range_destinazione,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    return result

# ✅ Legge e restituisce eventi ufficiali ordinati
def leggi_eventi_ufficiali(spreadsheet_id, range_dati, path_chiave_json):
    credentials = get_service_account_credentials(path_chiave_json)
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_dati
    ).execute()

    values = result.get("values", [])
    eventi = []

    for riga in values[1:]:  # Salta intestazione
        try:
            evento = {
                "giorno": int(riga[0]),
                "mese": int(riga[1]),
                "anno": int(riga[2]),
                "titolo": riga[3],
                "descrizione": riga[4],
                "link": riga[5],
                "immagine_url": riga[6]
            }
            eventi.append(evento)
        except IndexError:
            continue  # ignora righe incomplete

    eventi.sort(key=lambda e: (e["mese"], e["giorno"], e["anno"]))
    return eventi
