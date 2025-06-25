## Create .env with these variables
```
OPENAI_API_KEY= 
LANGSMITH_TRACING= FALSE
KMP_DUPLICATE_LIB_OK = TRUE
```
## Create credentials.json
- download the oauth id google credentials file and rename it to credentials.json in the root of the project.

# OAuth 

## Create Google Gmail Api Credentials and Authorization
 
Link:
https://console.cloud.google.com/

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

## Authorize an User In The Google Cloud Platform Credentials
- Authorize your email to access the application login.