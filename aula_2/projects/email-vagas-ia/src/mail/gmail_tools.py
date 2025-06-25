from langchain_google_community import GmailToolkit
from mail.credentials import GoogleCredentialProvider

class GmailTools:
    """
    GmailTools Class
    - This class provides a set of tools to interact with Gmail using the Gmail API.
    - It initializes the Gmail API toolkit with credentials fetched from the GoogleCredentialProvider.
    - The class includes methods to search for emails, get email messages by ID, send emails
        and mark emails as read.
    """
    def __init__(self):
        self.creds = GoogleCredentialProvider().fetch_credential()
        self.raw_toolkit = GmailToolkit(credentials=self.creds)
        self.tools = { tool.name: tool for tool in self.raw_toolkit.get_tools() }

    def search_tool(self):
        return self.tools["search_gmail"]
    
    def get_message_tool(self):
        return self.tools["get_gmail_message"]
    
    def send_email_tool(self):
        return self.tools["send_gmail_message"]
    
    def search_unread(self):
        return self.search_tool().run("label:inbox is:unread")
    
    def mark_as_read(self, msg_id):
        self.raw_toolkit.api_resource.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
        
    def get_email_by_id(self, msg_id):
        return self.get_message_tool().invoke(
            {"message_id": msg_id}
            )