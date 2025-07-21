# Aula 1 - Introdução a LLM Applications

## O que são LLMs?

**LLM** significa **Large Language Model**, ou em português, **Modelo de Linguagem de Grande Escala**.

### Definição simples:

São modelos de inteligência artificial treinados para **entender e gerar linguagem humana**.

Eles conseguem:

- Responder perguntas
    
- Escrever textos
    
- Traduzir línguas
    
- Completar códigos
    
- Raciocinar, resumir, dialogar…
    

Tudo isso a partir de **padrões de linguagem** aprendidos em **grandes volumes de dados** (livros, sites, artigos, códigos, etc.).

## Qual algoritmo está por trás das LLMs?

O **Transformer** é a arquitetura base que está por trás da maioria dos LLMs modernos.

É um modelo de deep learning apresentado no artigo:

> **"Attention is All You Need"** (Vaswani et al., 2017)

Ele introduziu um novo mecanismo chamado **self-attention**, que permite ao modelo entender o **contexto global** de uma sequência de palavras de forma eficiente.

## O que são **Prompts**?

Prompt é o texto de entrada que você envia para um LLM (Large Language Model) para obter uma resposta.

O **prompt é o roteiro**: quanto melhor for o roteiro, melhor será a atuação.

### Prompt Engineering

É a prática de **escrever prompts de forma estratégica** para guiar o comportamento do modelo.

- Escolher palavras certas
    
- Dar contexto
    
- Fornecer exemplos
    
- Especificar formato da resposta
- Guardrails 

```
Você é um assistente de atendimento ao cliente.
Responda educadamente, de forma objetiva e sempre com uma saudação.
Cliente: “Não consigo acessar minha conta”
```

### Como o prompt é processado pela LLM?
#### 1. **Tokenização**

- O prompt é dividido em **tokens**, usando um algoritmo como `tiktoken` (OpenAI) ou `SentencePiece`.
    
- Token ≠ palavra  
    Exemplo:
    
    - `"banana"` → 1 token
        
    - `"bananada"` → 2 tokens (`"banana"` + `"da"`)
        
    - `"GPT-4 é demais!"` → 7 tokens
        

> 🧠 LLMs operam **token por token**, não por palavra.

### Por que isso importa?

- **Preço** é cobrado por **token de entrada + saída**
    
- **Limite de contexto** também é em tokens (ex: 4096, 8k, 128k)
    
- **Prompt mal planejado** pode desperdiçar tokens.

Exemplo de contador de Tokens:
```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode("Eu gosto de café")
print(len(tokens), tokens)

```

## O que são LLM Applications?
 
**LLM Applications** são aplicações que usam **Large Language Models (LLMs)** como parte da lógica ou experiência do usuário.
 
São sistemas que aproveitam as capacidades de LLMs (como GPT-4, Claude, Mistral, etc.) para **entender, gerar ou transformar linguagem natural** — seja texto, código, comandos, ou dados semiestruturados.

O desenvolvedor pode unir o desenvolvimento tradicional ao uso das LLMs no seu código, tornando aplicações normais em aplicações inteligentes.

### Exemplos de LLM Applications:

| Aplicação                        | O que faz com LLM                                     |
| -------------------------------- | ----------------------------------------------------- |
| **Chatbots com persona**         | Atendimento, suporte técnico, terapeutas simulados    |
| **Assistentes de produtividade** | Agendam tarefas, organizam emails, geram relatórios   |
| **Classificadores inteligentes** | Identificam sentimentos, categorias, intenções        |
| **Agentes autônomos**            | Tomam decisões e executam ações (ex: agendar reunião) |
| **Sistemas RAG (Search + LLM)**  | Respondem perguntas com base em fontes confiáveis     |
| **Conversores de linguagem**     | Geração de código, SQL, traduções, resumos            |

## O que é o **LangChain**?

**LangChain** é um **framework em Python (e JS)** que facilita o desenvolvimento de **aplicações com LLMs** — como chatbots, agentes, RAGs e automações inteligentes.

Com LangChain vamos unir as LLMs a nossa logica de programação, criando sistemas complexos com o uso de IA de forma arquitetada.

### O que são **Chains**?

Uma **Chain** é uma **sequência de etapas** que processam informações com ajuda de um LLM — como se fosse um **pipeline de raciocínio ou execução**.

processo 1 | processo 2 | LLM | parser


## Projeto Prático

No nosso ambiente usaremos `pyenv` , `poetry`, `OpenAi` e `langchain`.

**Objetivo**: Criar um chat de conversa com LLM no Command line. 

Vamos ver na prática o uso de uma Chain e prompt engineer básicos para iniciar a jornada nas llm applications.

## O Novo Profissional: Dev + IA

### 1. **A fusão de habilidades**

O profissional de tecnologia hoje não é só programador:

> Ele é um **desenvolvedor que entende e domina IA generativa**, especialmente LLMs.

- Sabe escrever código eficiente
    
- **Sabe construir, ajustar e integrar modelos de linguagem**
    
- Entende **prompt engineering** como parte do desenvolvimento
    
- Combina lógica tradicional com inteligência artificial

### 2. **Por que isso é importante?**

- As empresas estão incorporando IA para **automatizar processos, melhorar UX e criar novos produtos**
    
- O mercado pede devs que saibam usar IA para resolver problemas reais, não só consumir APIs
    
- Habilidades em IA aumentam **competitividade, empregabilidade e inovação**
### 3. **Ferramentas e stacks comuns**

- Linguagens: Python (líder), JS/TS, Go
    
- Frameworks: LangChain, LangGraph, Hugging Face
    
- Serviços: OpenAI, Anthropic, Google Vertex AI
    
- DevOps: Monitoramento de tokens, custo e performance
