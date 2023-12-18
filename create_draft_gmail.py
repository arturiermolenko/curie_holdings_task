import base64
import os
from email.message import EmailMessage

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


class CreateDraft:
    _SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    _SERVICE_ACCOUNT_FILE = os.environ["SERVICE_ACCOUNT_FILE"]
    _TOKEN_FILE = os.environ["TOKEN_FILE"]
    _USER_ID = os.environ["USER_ID"]
    _MY_EMAIL = os.environ["MY_EMAIL"]

    def __init__(self,
                 subject: str,
                 email_address: str,
                 email_content: str, ):
        self.get_or_create_token()
        self.subject = subject
        self.email_address = email_address
        self.email_content = email_content

    def gmail_create_draft(self):
        """Create and insert a draft email.
         Print the returned draft's message and id.
         Returns: Draft object, including draft id and message metadata.

        Load pre-authorized user credentials from the environment.
        """
        # creds, _ = google.auth.default()
        creds = Credentials.from_authorized_user_file(self._TOKEN_FILE, self._SCOPES)

        try:
            # create gmail api client
            service = build("gmail", "v1", credentials=creds)

            message = EmailMessage()

            message.set_content(self.email_content)

            message["To"] = self.email_address
            message["From"] = self._MY_EMAIL
            message["Subject"] = self.subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"message": {"raw": encoded_message}}
            # pylint: disable=E1101
            draft = (
                service.users()
                .drafts()
                .create(userId=self._USER_ID, body=create_message)
                .execute()
            )

            print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        except HttpError as error:
            print(f"An error occurred: {error}")
            draft = None

        return draft

    def get_or_create_token(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self._TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(self._TOKEN_FILE, self._SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._SERVICE_ACCOUNT_FILE, self._SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self._TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            results = service.users().labels().list(userId=self._USER_ID).execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])

        except HttpError as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    my_draft = CreateDraft(
        subject=input("Subject:"),
        email_address=input("Address: "),
        email_content=input("Content: ")
    )
    my_draft.gmail_create_draft()
