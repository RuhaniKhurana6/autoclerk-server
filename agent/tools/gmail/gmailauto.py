import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64


class GmailAutomation:
    def __init__(self, creds_file: str = None, token_file: str = None):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.creds = None
        self.service = None

        # Default to the directory where this file lives
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.creds_file = creds_file or os.path.join(base_dir, "credentials.json")
        self.token_file = token_file or os.path.join(base_dir, "token.json")

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save new token
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("gmail", "v1", credentials=self.creds)
        return self.service

    def create_message(self, sender, to, subject, message_text, attachments=None):
        """Create an email message with optional attachments"""
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    message.attach(part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    def send_message(self, message):
        """Send an email message"""
        try:
            sent_message = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            return sent_message
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def list_messages(self, query=None, max_results=10):
        """List messages in the user's mailbox"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f'An error occurred: {e}')
            return []

    def get_message(self, msg_id):
        """Get a specific message by ID"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            return message
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def create_draft(self, message):
        """Create an email draft"""
        try:
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': message}
            ).execute()
            return draft
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def list_drafts(self, max_results=10):
        """List email drafts"""
        try:
            results = self.service.users().drafts().list(
                userId='me',
                maxResults=max_results
            ).execute()
            drafts = results.get('drafts', [])
            return drafts
        except Exception as e:
            print(f'An error occurred: {e}')
            return []

    def delete_message(self, msg_id):
        """Delete a specific message by ID"""
        try:
            self.service.users().messages().delete(
                userId='me',
                id=msg_id
            ).execute()
            return True
        except Exception as e:
            print(f'An error occurred: {e}')
            return False

    def modify_message_labels(self, msg_id, add_labels=None, remove_labels=None):
        """Modify the labels of a specific message"""
        try:
            if add_labels is None:
                add_labels = []
            if remove_labels is None:
                remove_labels = []

            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={
                    'addLabelIds': add_labels,
                    'removeLabelIds': remove_labels
                }
            ).execute()
            return True
        except Exception as e:
            print(f'An error occurred: {e}')
            return False
