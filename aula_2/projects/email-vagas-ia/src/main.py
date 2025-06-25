from watcher.gmail_watcher import GmailAiWatcher
from dotenv import load_dotenv

load_dotenv()

"""
Main entry point for the Gmail AI Watcher application.
This script initializes the GmailAiWatcher and starts the email watching process.
"""
if __name__ == "__main__":
    watcher = GmailAiWatcher()
    watcher.run()