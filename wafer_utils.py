import logging
from settings import WAFER_BASE_URL, WAFER_USERNAME, WAFER_PASSWORD
from requests.auth import HTTPBasicAuth
import requests

USER_LIST_URL = f"{WAFER_BASE_URL}/users/api/users/"
TICKET_LIST_URL = f"{WAFER_BASE_URL}/tickets/api/tickets/"


def fetch_all_pages(url):
    results = []
    while url is not None:
        logging.info(f"fetching: {url}")
        response = requests.get(url, auth=HTTPBasicAuth(WAFER_USERNAME, WAFER_PASSWORD))
        assert response.status_code == 200, f"{response} {response.content}"
        data = response.json()
        results.extend(data["results"])
        url = data["next"]
    return results


def fetch_all_users_and_ticket_emails(ticket_holders_only):
    results = fetch_all_pages(TICKET_LIST_URL)
    if not ticket_holders_only:
        results.extend(fetch_all_pages(USER_LIST_URL))
    return [d["email"] for d in results]
