# TODO
- Criar GMAIL pra.vagas.1@gmail.com
- Criar API KEY do Gmail
- Criar Rag com meu Currículo
- Criar codigo langchain que acessa o gmail
- Criar prompt que difere se o email é sobre oportunidade de trabalho ou nao

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