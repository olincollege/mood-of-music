"""
Exporting Spotify Playlist Links from Survey Results
"""
from __future__ import print_function

import os.path
import requests
import validators
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1aGhKcdd-hFxZggOMNydM2ElF2gU0IO6JkkWo3SN6RZA"
RANGE_YEAR = "C2:F"
RANGE_EMAIL = "B2:G"


def link_testing(playlist_link):
    """
    Filter through invalid, non-Spotify, or private playlist links.

    Args:
        playlist_link: A string representing the playlist link.

    Returns:
        A boolean value of whether the link is valid or not.
    """
    if not validators.url(playlist_link):
        return False
    link = requests.get(playlist_link, timeout=10)
    if link.status_code != 200:
        return False
    if "open.spotify.com" not in playlist_link:
        return False

    return True


def googlesheet_authenticate():
    """
    Authenticate Google Account with Google Sheets API token
    and creates a token file if none exists.

    Returns:
        A Resource object for interacting with the Google Sheets API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_spreadsheet.json"):
        creds = Credentials.from_authorized_user_file("token_spreadsheet.json", SCOPES)
        return creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_899143637035-ehhtn86j8tcglm9uhne3n3vc0d0kevbm.apps.googleusercontent.com.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token_spreadsheet.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
        return creds


def googlesheet_email():
    """
    Return a dictionary of survey response emails and their playlist links

    Returns:
        A dicitionary with user email as keys and playlist links as values
    """
    creds = googlesheet_authenticate()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        results = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_EMAIL)
            .execute()
        )

        return results["values"]

    except HttpError as err:
        return print(err)


googlesheet_email()


def googlesheet_by_year():
    """
    Return a dictionary of Spotify Playlist links according to the specifc year
    the playlist was made

    Returns:
        A dictionary with years(2019,2020,2021,2022) as keys
        and playlist links as values

    """
    creds = googlesheet_authenticate()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_YEAR).execute()
        )

        # Categorize the playlists into their specific years into a library
        shelf = {"2019": [], "2020": [], "2021": [], "2022": []}
        for play in result["values"]:
            fill = (4 - len(play)) * [""]
            if len(play) < 4:
                play.extend(fill)
            if len(play) > 1:
                shelf["2019"].append(play[0])
                shelf["2020"].append(play[1])
                shelf["2021"].append(play[2])
                shelf["2022"].append(play[3])
        # Get rid of empty response for specific year
        for year, link in shelf.items():
            link = [full for full in link if full != ""]
            shelf[year] = link
        # Get rid of invalid links using the link testing function defined above
        for year, link in shelf.items():
            link = [item for item in link if link_testing(item) is True]
            shelf[year] = link

        return shelf

    except HttpError as err:
        return print(err)
        exit()
