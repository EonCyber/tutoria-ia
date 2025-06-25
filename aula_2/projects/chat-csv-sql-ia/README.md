## Crie .env com estas variáveis
```
DB_PATH=src/db/sample.db
DATA_PATH=src/data
OPENAI_API_KEY= 
LANGSMITH_TRACING= FALSE
KMP_DUPLICATE_LIB_OK = TRUE
```

## Desafio
- Otimize as chains com RAG para evitar um saturamento da janela de contexto, caso o numero de tabelas seja muito maior.