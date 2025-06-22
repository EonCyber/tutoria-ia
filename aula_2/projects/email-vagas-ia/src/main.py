from watcher.gmail_watcher import GmailAiWatcher
from dotenv import load_dotenv

load_dotenv()



if __name__ == "__main__":
    watcher = GmailAiWatcher()
    watcher.run()