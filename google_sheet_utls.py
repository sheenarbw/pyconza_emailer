import logging
import gspread


def fetch_sheet(sheet: str = None, url: str = None):
    print(f"Fetching sheet: {sheet} {url}")
    service = _get_gspread_service()
    if sheet:
        book = service.open(sheet)
    elif url:
        book = service.open_by_url(url)
    else:
        raise Exception("Must provide url or sheet name")
    logging.info(f"fetched sheet {sheet}")
    sheet = book.sheet1  # choose the first sheet
    return sheet.get_all_records()


def _get_gspread_service():
    credentials = _authorize_creds()
    ret = gspread.authorize(credentials)
    return ret


def _authorize_creds():
    import json
    from oauth2client.client import SignedJwtAssertionCredentials
    import os

    SCOPE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    SECRETS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")

    if not SECRETS_FILE:
        raise Exception(
            "Missing environmental variable: GOOGLE_SHEETS_CREDENTIALS_FILE"
        )

    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    # Load in the secret JSON key in working directory (must be a service account)
    json_key = json.load(open(SECRETS_FILE))

    # Authenticate using the signed key
    credentials = SignedJwtAssertionCredentials(
        json_key["client_email"], json_key["private_key"], SCOPE
    )
    return credentials
