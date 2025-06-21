# TODO
- Criar GMAIL pra.vagas.1@gmail.com
- Criar API KEY do Gmail
- Criar Rag com meu Currículo
- Criar codigo langchain que acessa o gmail
- Criar prompt que difere se o email é sobre oportunidade de trabalho ou nao


# GMAIL
tutoriaiagenerativa@gmail.com
P5Li9&RT$psrsX
# OAuth

# Criar Credenciais Google Gmail
 
Link:
https://console.cloud.google.com/welcome/new?pli=1&inv=1&invt=Ab0jHg

🛠️ 1. Create a Google Cloud Project & Enable Gmail API
- Sign in to the [Google Cloud Console].

- Click the project selector at the top → Create Project → give it a name → Create.

- In the left menu, go to **APIs & Services** → Library, search for Gmail API and click Enable

🔑 2. Create Credentials (OAuth Client ID)
- OAuth 2.0 Client ID (recommended for Gmail access)
In the same credentials page, choose Create Credentials → OAuth client ID.

- You’ll configure the OAuth consent screen, then choose application type (e.g. Desktop app).

- After creation, you'll download a credentials.json containing a Client ID and Client Secret for full access to user Gmail via OAuth

💸 3. Cost & Usage
**Free to use**: The Gmail API itself is free—including reading and sending emails.

# Poll Example 
```python
# Poll inbox
seen = set()
while True:
    # 1. Search unread emails
    res = gmail_search.run("label:inbox is:unread")
    messages = eval(res) if isinstance(res, str) else res

    for m in messages:
        msg_id = m["id"]
        if msg_id in seen:
            continue
        seen.add(msg_id)

        # 2. Fetch full message (including thread and sender)
        msg = gmail_getmsg.run({"id": msg_id})
        payload = msg.get("payload", {})
        raw = payload.get("body", {}).get("data", "")
        thread_id = msg.get("threadId")
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        sender = headers.get("From", "").split("<")[-1].rstrip(">")

        # Clean HTML to text
        body_text = BeautifulSoup(raw, "html.parser").get_text()

        # 3. Generate summary
        summary = llm_chain.run(email_body=body_text)

        # 4. Reply in-thread with summary
        gmail_send.run({
            "to": sender,
            "subject": "Re: " + headers.get("Subject", ""),
            "message": summary,
            "threadId": thread_id
        })

        print(f"Replied to {sender} in thread {thread_id}")

    time.sleep(30)  # Poll every 30 seconds
```