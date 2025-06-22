
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import json
from util.stdout import logtext

OAUTH_TOKEN_PATH = 'token.json'
CREDENTIALS_JSON_PATH = 'credentials.json'
MODIFY_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'

class GoogleCredentialProvider:
    
    def __init__(self):
        self.scopes = [MODIFY_SCOPE]
        self.creds = None

    def fetch_credential(self):
        logtext("Fetching Google Credentials from local assets...")
        if Path(OAUTH_TOKEN_PATH).exists():
            logtext("Token Found. Authorizing...")
            with open(OAUTH_TOKEN_PATH, "r") as token:
                token_data = json.load(token)
                self.creds = Credentials.from_authorized_user_info(info=token_data, scopes=self.scopes)
                logtext("Success: Authorization OK!")
        if not self.creds or not self.creds.valid:
            logtext("Warning: Credentials are Invalid or Token not Found.")
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logtext("Warning: Token Expired. Genereting Refresh Token...")
                self.creds.refresh(Request())
            else:
                logtext("Warning: Authenticating Token not found. Generating new Token.")
                if Path(CREDENTIALS_JSON_PATH).exists():
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON_PATH, self.scopes)
                    self.creds = flow.run_local_server(port=56632)
                    with open(OAUTH_TOKEN_PATH, "w") as token:
                        token.write(self.creds.to_json())
                    logtext("Success: Authorization OK!")
                else:
                    raise RuntimeError("Error: Credentials Json not Found on Local assets!")
        return self.creds 
        