"""
Function for sending emails about Playlist results.
"""
from __future__ import print_function
import os
import base64
import numpy

from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from requests import HTTPError
from google_auth_oauthlib.flow import InstalledAppFlow
from google_spreadsheet import googlesheet_email
from main import average_valence

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gmail_authenticate():
    """
    Authenticate Google Account with Gmail API token and creates a token file if none exists.

    Returns:
        A Resource object for interacting with the Gmail API.

    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token_gmail.json"):
        creds = Credentials.from_authorized_user_file("token_gmail.json", SCOPES)
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
        with open("token_gmail.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def generate_email_list():
    """
    Filter out responses that did not submit an email.

    Returns:
        A list of lists with links and email addresses.
    """
    email_list = []
    emails = googlesheet_email()
    for email in emails:
        if len(email) > 1 and len(email) == 6:
            email_list.append(email)
    return email_list


def gmail_write():
    """
    Use Gmail API to send a email with the Playlist Mood Analysis results.
    """
    service = gmail_authenticate()
    email_list = generate_email_list()
    try:
        for recipient in email_list:
            if recipient[0] != "":
                name = recipient[0]
            else:
                name = "Mysterious Stranger"
            year19 = average_valence(recipient[1])
            year20 = average_valence(recipient[2])
            year21 = average_valence(recipient[3])
            year22 = average_valence(recipient[4])
            message = MIMEText(
                f"Hey {name}!"
                "\n"
                "\n"
                "We are the YourMoodOfMusic SoftDes Team, and you are "
                "recieving this email because you responded back to our survey."
                "\n"
                "\n"
                "Our project aimed to determine how happy a person was"
                "in a specifc year based on their Spotify Wrapped."
                "\n"
                "\n"
                "We used 'valence' values,provided by Spotify, to calculate the average 'happiness "
                "value of the songs in your playlist."
                "\n"
                "\n"
                "These valence values range from 0 to 1, with higher "
                "scores meaning more happiness!"
                "\n"
                "\n"
                "For those of you who were curious about your "
                "own valence scores...Here are the results!"
                "\n"
                "\n"
                f"In 2019, you were about {year19} happy."
                "\n"
                "\n"
                f"In 2020, you were about {year20} happy"
                "\n"
                "\n"
                f"In 2021, you were about {year21} happy"
                "\n"
                "\n"
                f"In 2022, you were about {year22} happy"
                "\n"
                "\n"
                "\n"
                "Thank you for being part of our project!"
            )
            message["to"] = recipient[-1]
            message["from"] = "The MoodOfMusic Team"
            message["subject"] = "Your Mood of Music Results!"

            create_message = {
                "raw": base64.urlsafe_b64encode(message.as_bytes()).decode()
            }

            message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )

    except HTTPError as error:
        print(f"An error occurred: {error}")
        message = None


if __name__ == "__main__":
    gmail_write()
