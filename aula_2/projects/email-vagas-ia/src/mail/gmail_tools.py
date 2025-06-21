from langchain_google_community import GmailToolkit
from mail.credentials import GoogleCredentialProvider
from util.stout import logtext

class GmailTools:
    
    def __init__(self):
        self.creds = GoogleCredentialProvider().fetch_credential()
        self.tools = { tool.name: tool for tool in GmailToolkit(credentials=self.creds).get_tools() }

    def search_tool(self):
        logtext('Generating: Gmail Search Tool.')
        return self.tools["gmail_search"]
    
    def get_message_tool(self):
        logtext('Generating: Gmail Get Message Tool.')
        return self.tools["gmail_get_message"]
    
    def send_email_tool(self):
        logtext('Generating: Gmail Send Message Tool.')
        return self.tools["gmail_send_message"]