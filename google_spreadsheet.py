"""
Exporting Spotify Playlist Links from Survey Results
"""
from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1aGhKcdd-hFxZggOMNydM2ElF2gU0IO6JkkWo3SN6RZA"
RANGE_NAME = "C2:F"


def googlesheet():
    """
    Return a dictionary of Spotify Playlist links according to the specifc year
    the playlist was made

    Args:
        Any parameter

    Returns:
        A dictionary with years(2019,2020,2021,2022) as keys
        and playlist links as values

    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )

        # Categorize the playlists into their specific years into a library
        shelf = {"2019": [], "2020": [], "2021": [], "2022": []}
        for play in result["values"]:
            fill = (4 - len(play)) * [""]
            if len(play) < 4:
                play.extend(fill)
            if len(play) > 1:
                print(play)
                shelf["2019"].append(play[0])
                shelf["2020"].append(play[1])
                shelf["2021"].append(play[2])
                shelf["2022"].append(play[3])

        # Get rid of empty response for specific year
        for year, link in shelf.items():
            link = [full for full in link if full != ""]
            shelf[year] = link

        return print(shelf)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    googlesheet()
