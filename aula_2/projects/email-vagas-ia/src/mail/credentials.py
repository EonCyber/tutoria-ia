
import os.path
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from util.stout import logtext
class GoogleCredentialProvider:
    
    def __init__(self):
        self.oauth_token = '/assets/token.json'
        self.cred_path = '/assets/credentials.json'
        self.scopes = ['https://www.googleapis.com/auth/gmail.modify']
        self.creds = None

    def fetch_credential(self):
        logtext("Fetching Google Credentials from local assets...")
        if os.path.exists(self.oauth_token):
            self.creds = Credentials.from_authorized_user_file(self.cred_path, self.scopes)
            logtext("Success: Credentials OK!")
        if not self.creds or not self.creds.valid:
            logtext("Warning: Credentials are Invalid or Token not Found.")
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logtext("Warning: Token Expired. Genereting Refresh Token...")
                self.creds.refresh(Request())
            else:
                logtext("Warning: Authenticating Token not found. Generating new Token.")
                if os.path.exists(self.oauth_token):
                    flow = InstalledAppFlow.from_client_secrets_file(self.cred_path, self.scopes)
                    self.creds = flow.run_local_server(port=0)

                    with open(self.oauth_token, "w") as token:
                        token.write(self.creds.to_json())
                else:
                    raise RuntimeError("Error: Credentials Json not Found on Local assets!")
        
        return self.creds 
        