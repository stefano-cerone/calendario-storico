from google.oauth2 import service_account
from googleapiclient.discovery import build

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
