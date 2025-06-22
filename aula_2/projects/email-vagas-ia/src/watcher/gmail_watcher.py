from watcher.llm import RagContextChain
from rag.rag import CVRetrieval
from mail.gmail_tools import GmailTools
from util.stdout import logaianswer,loginputtext,logtext

DOC_PATH = 'assets/cv.docx'

class GmailAiWatcher:
    
    def __init__(self):
        self.tools = GmailTools()
    
    def run(self):
        seen = set()
        logtext('Configurando Watcher...')
        # * Email Tools Configuration
        logtext('Setting Gmail Tools...')
        gmail_send = self.tools.send_email_tool()
        # =====================================
        # * Rag Configuration
        logtext('Configuring RAG-LLM-Chain...')
        cv_retrieval = CVRetrieval(DOC_PATH)
        cv_retrieval.load_retriever()
        retriever = cv_retrieval.fetch_retriever()
        rag = RagContextChain(retriever)
        # =====================================
        # * Watcher Logic
        logtext('Aguardando mensagem...')
        while True:
             res = self.tools.search_unread()
             messages = eval(res) if isinstance(res, str) else res

             for m in messages:
                msg_id = m["id"]
                if msg_id in seen:
                    continue
                seen.add(msg_id)
                self.tools.mark_as_read(msg_id)
                # 2. Fetch full message (including thread and sender)
                msg = self.tools.get_email_by_id(msg_id)
                # Data and Metadata
                raw = msg.get("body")
                subject = msg.get("subject")
                thread_id = msg.get("threadId")
                sender = msg.get("sender")

                # Clean HTML to text
                # body_text = BeautifulSoup(raw, "html.parser").get_text()
                body_text = raw

                # 3. Generate rag response
                logtext('\n\n**New Email Received**:')
                loginputtext(f'Assunto: {subject}\n')
                loginputtext(f'{body_text}\n')
                email_answer = rag.answer(body_text)
                logaianswer(email_answer)

                # 4. Reply Email Message
                result = gmail_send.invoke({
                    "to": [sender],
                    "subject": f"Re: {subject}",
                    "message": email_answer,
                    "threadId": thread_id
                })
                logaianswer(result)


       