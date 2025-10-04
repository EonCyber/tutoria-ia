#mentoriafire  #agentes #aula #context #curso 


## Conceitos básicos 

### 1. Memória de curto prazo (conversa corrente)

1. **Definição:** espaço limitado ao contexto da chamada do modelo.
    
2. **Limite técnico:** cada LLM possui um número máximo de _tokens_ que podem ser enviados no prompt.
    
3. **Desafios:**
    
    - Se a conversa ultrapassa o limite, o histórico precisa ser cortado.
        
    - A escolha do que manter afeta a coerência das respostas.
        
4. **Práticas comuns:**
    
    - _Sliding window_: manter apenas as últimas interações.
        
    - _Buffer de resumo_: reduzir o histórico a um texto condensado.
        
5. **Exemplo prático:** 
   Um agente de captura de informacoes e manda via API pra um servico. (Essas informações não precisam estar guardadas pelo agente para as proximas conversas.)
   Tradução: que envolva contexto da informação traduzida. Tradução por etapas. 
   Sistema de Geracao de Animacoes: A cada sessao, ele gera animacoes por etapas.
	Prontuario: 

---

### 2. Memória de longo prazo (persistência externa)

1. **Definição:** armazenamento de informações que precisam sobreviver a várias sessões.
    
2. **Formas de implementação:**
    
    - Bancos relacionais (SQLite, Postgres).
        
    - Document stores (MongoDB, DynamoDB).
        
    - Bases em arquivos JSON/YAML para protótipos.
        
3. **Uso típico:**
    
    - Preferências do usuário (idioma, estilo de resposta).
        
    - Histórico de projetos ou tickets em um sistema de suporte.
        
4. **Risco:** acúmulo de dados irrelevantes gera _ruído_. É necessário definir políticas de retenção.
    
5. **Exemplo prático:** um assistente de estudo que lembra quais capítulos o aluno já leu.
    

---

### 3. Memória semântica via embeddings (RAG)

1. **Definição:** transformar textos em vetores de alta dimensão para busca por similaridade.
    
2. **Infraestrutura:** FAISS, Milvus, Weaviate, Pinecone.
    
3. **Vantagens:**
    
    - Escala: pode armazenar milhões de interações.
        
    - Recupera informações conceitualmente próximas, não só palavras idênticas.
        
4. **Uso prático:**
    
    - Chatbots que respondem com base em documentos internos.
        
    - Agentes que lembram contextos passados semelhantes.
        
5. **Exemplo:** ao perguntar “qual era a recomendação do médico?”, o sistema recupera a nota “tomar vitamina D diariamente”, mesmo sem a palavra “recomendação”.
    

---

### 4. Memória hierárquica e compressão de histórico (avançado)

1. **Problema:** longas interações enchem a memória de curto prazo.
    
2. **Solução:** criar camadas de memória:
    
    - **Nível imediato:** últimas falas do usuário.
        
    - **Nível resumido:** sumários de blocos de conversa.
        
    - **Nível episódico:** eventos relevantes (“viagem a Paris em julho”).
        
3. **Técnicas:**
    
    - _Summarization-on-the-fly_: resumos incrementais automáticos.
        
    - _Clusterização semântica_: agrupar interações semelhantes.
        
    - _Memory decay_: expirar dados antigos ou irrelevantes.
        
4. **Benefício:** reduz custo e mantém contexto consistente em interações longas.
    
5. **Exemplo prático:** um agente pessoal que, após meses, ainda “lembra” dos objetivos de estudo do usuário sem precisar carregar cada conversa.
    

---

### 5. Memória multimodal e múltiplos contextos (avançado)

1. **Definição:** memória que abrange não só texto, mas também imagens, áudio, código, resultados de ferramentas.
    
2. **Aplicação em agentes:**
    
    - Memória de **planejamento**: próximos passos da execução.
        
    - Memória de **execução**: logs do que já foi feito.
        
    - Memória **do usuário**: preferências e restrições.
        
3. **Integração multimodal:**
    
    - Salvar embeddings de imagens ou áudios (CLIP, Whisper).
        
    - Reutilizar resultados de código (ex.: cache de chamadas API).
        
4. **Desafios:**
    
    - Normalizar diferentes formatos de dados.
        
    - Definir quando e como reutilizar essas memórias.
        
5. **Exemplo prático:** um agente que ajuda no design guarda não só a conversa, mas também _sketches_ anteriores e feedback do cliente.
--- 
# Extras
### 6. Controle de privacidade e retenção de memória

- **Problema:** armazenar tudo pode violar privacidade ou regulamentos (LGPD, GDPR).
    
- **Práticas:**
    
    - Definir tempo de expiração (_memory TTL_).
        
    - Permitir ao usuário “apagar memória”.
        
    - Diferenciar o que é “memória do sistema” e “memória pessoal”.
        

### 7. Indexação híbrida (texto + semântica)

- Combinar **busca lexical** (palavra-chave) com **busca vetorial** (similaridade semântica).
    
- Melhora precisão em casos de termos técnicos ou nomes próprios.
    
- Exemplo: recuperar "RFC 2616" tanto por “HTTP spec” quanto pelo número.
    

### 8. Consistência entre memória e realidade

- **Risco:** modelo confiar em lembranças desatualizadas.
    
- **Solução:**
    
    - Validar informações antigas contra fontes externas (API, banco de dados).
        
    - Manter versões ou carimbos de data/hora.
        

### 9. Memória compartilhada entre agentes

- Em arquiteturas multi-agente, é comum precisar de uma **memória coletiva**.
    
- Tipos:
    
    - **Memória centralizada:** todos acessam o mesmo repositório.
        
    - **Memória segmentada:** cada agente guarda a sua e compartilha só o necessário.
        

### 10. Performance e custo da memória

- Mais memória = mais dados no prompt = mais tokens = mais custo.
    
- Estratégias de otimização:
    
    - Resumir antes de enviar ao LLM.
        
    - Carregar apenas _chunks_ relevantes via busca semântica.
        
    - Cachear resultados comuns.

--- 

### Memória e melhoria por feedback

Sim, memória **habilita um ciclo de feedback** que melhora a interação:

1. **Registro de preferências:** usuário pode corrigir o agente (“Não gosto de respostas longas”) → agente guarda e ajusta comportamento.
    
2. **Aprendizado incremental:** feedback (“essa resposta não ajudou”) pode ser registrado e usado para futuras consultas.
    
3. **Correção de erros recorrentes:** se o usuário corrige algo repetidamente, a memória pode servir como “patch” permanente.
    
4. **Customização contínua:** o assistente evolui junto ao usuário, criando uma experiência mais natural e eficiente.

### Casos práticos de memória

1. **Chatbots de atendimento**
    
    - Curto prazo: lembra das últimas perguntas para manter a coerência.
        
    - Longo prazo: armazena histórico de interações de cada cliente.
        
    - Uso: evitar que o cliente repita dados já informados (CPF, pedido).
        
2. **Assistentes pessoais**
    
    - Guarda preferências de agenda, estilo de comunicação, hábitos.
        
    - Exemplo: “Marque reuniões sempre às 10h” → o assistente aplica sem precisar repetir.
        
3. **Sistemas educacionais**
    
    - Memória registra os tópicos já estudados.
        
    - Exemplo: tutor de matemática lembra que o aluno tem dificuldade em frações.
        
4. **Agentes de programação**
    
    - Guardam contexto do projeto: decisões arquiteturais, bibliotecas escolhidas.
        
    - Exemplo: não sugerir `Flask` depois que já se decidiu usar `FastAPI`.
        
5. **Colaboração multiagente**
    
    - Vários agentes compartilham um espaço de memória para alinhar informações.
        
    - Exemplo: em um sistema de vendas, um agente lida com preços e outro com logística, ambos consultam o mesmo “cliente X pediu produto Y”.

# Prática Aplicando Memória no Langgraph
### 1. Habilitar Memória de Curto Prazo (Thread-Level)


```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

graph.invoke(
    {"messages": [HumanMessage(content="Oi!") ]},
    {"configurable": {"thread_id": "user-1"}}
)
```

### **Resumo Comparativo da Janela de Contexto**

| Aspecto              | Curto Prazo            | Longo Prazo                           |
| -------------------- | ---------------------- | ------------------------------------- |
| Histórico enviado    | Toda a thread atual    | Somente memórias relevantes filtradas |
| Limite               | LLM context window     | LLM context window + resumo/ranking   |
| Risco de truncamento | Alto se conversa longa | Alto se enviar muitas memórias        |
| Estratégia de uso    | Enviar tudo ou resumir | Filtrar, rankear e resumir            |