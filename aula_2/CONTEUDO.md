### 🎯 Objetivo da Aula

- Compreender o que é RAG e sua importância.
    
- Aprender como construir um pipeline básico de RAG.
    
- Explorar técnicas avançadas de otimização e boas práticas para produção.

## 🧩 Parte 1: Fundamentos de RAG

### 1.1 O que é RAG?

**Definição:**  
Retrieval-Augmented Generation é uma técnica que combina modelos de linguagem com mecanismos de recuperação de documentos para responder perguntas com base em dados externos (contexto), fora do conhecimento treinado.

**Motivação:**

- Grandes LLMs esquecem fatos recentes ou específicos.
    
- RAG permite incorporar contexto relevante dinamicamente.
    

**Arquitetura Básica:**

1. **Query → Retriever → Context**
    
2. **Context + Query → LLM → Resposta**
    

Use um diagrama simples para mostrar esse fluxo.

---
Racional:
### ❓O que falta às LLMs?

Modelos de linguagem como GPT, Claude, Gemini e LLaMA são impressionantes, mas têm **três limitações fundamentais**:

1. **Memória Estática (Conhecimento Congelado)**
    
    - LLMs aprendem com os dados de seu treinamento.
        
    - Esses dados têm um corte temporal (ex: GPT-4 cortado em 2023-04).
        
    - Não conhecem fatos recentes ou informações específicas de bases privadas.
        
2. **Limite de Conhecimento Específico ou Profundo**
    
    - Mesmo com bilhões de parâmetros, LLMs não armazenam cada detalhe de cada área do conhecimento.
        
    - Fatos muito específicos, técnicos ou confidenciais (como manuais internos, contratos ou bases científicas) **não são acessíveis**.
        
3. **Falta de Personalização**
    
    - LLMs são generalistas.
        
    - Elas não sabem nada sobre o seu domínio específico, sua empresa, seu cliente ou seu caso de uso sem contexto externo.

## 📚 O que é RAG (Retrieval-Augmented Generation)?

**RAG** é uma técnica que combina **Language Models (LLMs)** com **Information Retrieval**, permitindo que o modelo gere respostas com base em dados externos, mesmo que esses dados não estejam no seu treinamento original.

### 1.2 Componentes Principais

- **Retriever** (ex: FAISS, Weaviate, Elasticsearch, Chroma)
    
- **Embedding Models** (ex: `text-embedding-ada-002`, `all-MiniLM-L6-v2`)
    
- **Vector Store** (armazenamento e busca vetorial)
    
- **LLM** (ex: GPT-4, Mistral, LLaMA)

Racional:

## 🧠O que são **Embedding Models**?

Modelos de embedding são modelos de linguagem treinados para **converter textos em vetores numéricos** de alta dimensão. Esses vetores preservam **relações semânticas**, ou seja, textos com significados semelhantes terão vetores próximos no espaço vetorial.

Aqui estão os **melhores modelos de embedding** (até meados de 2025) para sistemas RAG, divididos entre soluções proprietárias e open-source, com base em benchmarks (MTEB, BEIR) e artigos recentes:

---

## 🚀 Embeddings Proprietários (Alta performance)

1. **Google Gemini embedding**
    
    - Aponta como _top performer_ em benchmarks de recuperação [writingmate.ai+9arxiv.org+9arxiv.org+9](https://arxiv.org/abs/2505.13482?utm_source=chatgpt.com)[modal.com+2research.aimultiple.com+2techrepublic.com+2](https://research.aimultiple.com/retrieval-augmented-generation/?utm_source=chatgpt.com).
        
2. **Voyage-3-large**
    
    - “Surpresa no topo” da Astra DB, sendo o líder em relevância [unstructured.io+8datastax.com+8mongodb.com+8](https://www.datastax.com/blog/best-embedding-models-information-retrieval-2025?utm_source=chatgpt.com).
        
3. **OpenAI text-embedding-3-large**
    
    - Dimensionalidade configurável, MRL, desempenho alto em MTEB [en.wikipedia.org+15mongodb.com+15vectorize.io+15](https://www.mongodb.com/developer/products/atlas/choose-embedding-model-rag/?utm_source=chatgpt.com).
        

---

## 🌐 Melhores modelos Open‑Source

1. **intfloat/e5-large-v2**
    
    - Muito eficiente e versátil para RAG [okareo.com+15modal.com+15writingmate.ai+15](https://modal.com/blog/embedding-models-article?utm_source=chatgpt.com).
        
2. **Salesforce/SFR-Embedding-2_R**
    
    - Forte em recuperação semântica [ukad-group.com+13modal.com+13mongodb.com+13](https://modal.com/blog/embedding-models-article?utm_source=chatgpt.com).
        
3. **intfloat/multilingual-e5-large-instruct**
    
    - Excelente para cenários multilíngues [modal.com](https://modal.com/blog/embedding-models-article?utm_source=chatgpt.com)[baseten.co](https://www.baseten.co/blog/the-best-open-source-embedding-models/?utm_source=chatgpt.com).
        
4. **BAAI bge-en-icl**
    
    - “Melhor modelo geral” open‑source, usado como referência [arxiv.org+2baseten.co+2modal.com+2](https://www.baseten.co/blog/the-best-open-source-embedding-models/?utm_source=chatgpt.com).
        
5. **Dewey long-context model**
    
    - Suporta janelas longas (até 128k tokens), ótimo para documentos extensos [en.wikipedia.org+15arxiv.org+15arxiv.org+15](https://arxiv.org/abs/2503.20376?utm_source=chatgpt.com).
        

---

## 🧠 Modelos Especializados

- **MedEIR**
    
    - Embedding médico, com contexto longo e precisão em textos científicos .
        
- **E5 family (E5-base, E5-large)**
    
    - Bem testados em BEIR/MTEB, robustos para busca zero-shot [en.wikipedia.org+11arxiv.org+11okareo.com+11](https://arxiv.org/abs/2212.03533?utm_source=chatgpt.com).
        
- **OpenAI text-embedding-3-large**
    
    - Embedding configurável (3072 dimensões), instrução-tuned [arxiv.org+15mongodb.com+15datastax.com+15](https://www.mongodb.com/developer/products/atlas/choose-embedding-model-rag/?utm_source=chatgpt.com).

## 📚 **Vector Store**

### O que é:

O **Vector Store** é o banco de dados onde ficam armazenados os vetores dos documentos (gerados por embeddings). Ele permite fazer buscas vetoriais de forma eficiente.

### Como funciona:

- Cada documento/chunk é representado por um vetor.
    
- Quando uma query chega, o vetor dela é comparado com todos os vetores no banco para encontrar os mais similares.
---
## 🚀 Parte 2: Uso Avançado e Otimização

### 2.1 Limitações do RAG Padrão

- Recuperações irrelevantes
    
- Contexto irrelevante ou muito extenso (Token Overflow)
    
- Alucinações mesmo com contexto
    
- Custo e latência em produção

### 2.2 Estratégias de Otimização

#### 🔎 Otimização do Retrieval

- **Reranking com Cross-Encoder** (colBERT, Cohere Rerank)
    
- **Multivector Indexing**: tokenizar documentos em múltiplos chunks semânticos
    
- **Hybrid Search**: Combinar vetorial + BM25
    

#### 📏 Otimização do Contexto

- **Chunking semântico**: usar títulos, subtópicos, heading-tags para corte inteligente
    
- **Maximizar conteúdo por token útil**
    
- **Score Filtering** com limiares de similaridade
    

#### 🧠 Prompt Engineering

- **Injectar o contexto com delimitação clara** (e.g. `### CONTEXTO`)
    
- **Instruções para usar apenas informações do contexto**
    
- **Few-shot RAG**: exemplos de uso no contexto


### 2.3 Arquiteturas Avançadas

- **Conversational RAG**: histórico mantido com memória e re-query
    
- **RAG em Grafos de Conhecimento**: integração com bases estruturadas
    
- **RAG + Agent (Tool use)**: uso de ferramentas baseado em contexto retornado

### 2.4 Métricas de Avaliação

- **Precision/Recall do Retrieval**
    
- **ROUGE, BLEU, BERTScore para geração**
    
- **Groundedness & Faithfulness**
    
- **Ragas (Retrieval-Augmented Generation Assessment Score)**

### 2.5 Casos de Uso no Mundo Real

- Chatbots jurídicos, médicos, financeiros
    
- Pesquisa em bases científicas
    
- Análise de documentos corporativos
## 🧩 Arquiteturas Avançadas de RAG

### 1. Retrieve‑and‑Rerank (Dois Estágios)

- **Fluxo**: busca rápida com bi‑encoder → reranking com cross‑encoder → LLM.
    
- **Prós**: alta precisão ao filtrar ruído.
    
- **Contras**: maior latência e complexidade operacional [arxiv.org+15skphd.medium.com+15medium.com+15](https://skphd.medium.com/different-rag-architectures-every-ai-professional-should-know-04f228e50fc3?utm_source=chatgpt.com).
    

---

### 2. Multimodal RAG

- **Descrição**: incorpora dados não textuais (imagens, vídeos, áudios). Usa modelos como CLIP, Flamingo para embeddings.
    
- **Uso**: correto em manuais técnicos, tutoria interativa.
    
- **Desafio**: requer alinhamento de embeddings e infraestrutura multimodal [skphd.medium.com+1github.com+1](https://skphd.medium.com/different-rag-architectures-every-ai-professional-should-know-04f228e50fc3?utm_source=chatgpt.com).
    

---

### 3. Graph‑based RAG

- **Descrição**: documentos são nós em um grafo; são realizadas buscas semânticas + travessia no grafo.
    
- **Vantagem**: excelente para raciocínio multi-hop e relações estruturadas entre documentos.
    
- **Exemplo**: PankRAG resolve sub-perguntas hierarquicamente, reranking dependente de relações [skphd.medium.com](https://skphd.medium.com/different-rag-architectures-every-ai-professional-should-know-04f228e50fc3?utm_source=chatgpt.com)[arxiv.org+1skphd.medium.com+1](https://arxiv.org/abs/2506.11106?utm_source=chatgpt.com).
    
- **Outra abordagem**: GeAR faz expansão via grafo e agentes para recuperação multi-hop [github.com+15arxiv.org+15arxiv.org+15](https://arxiv.org/html/2501.09136v1?utm_source=chatgpt.com).
    

---

### 4. Hybrid RAG (Vetorial + Grafo)

- **Fluxo**: busca vetorial + travessia de grafo + mescla dos resultados.
    
- **Benefícios**: combina profundidade semântica e estrutura relacional.
    
- **Caso real**: projeto com FAISS + BM25 + Knowledge Graph + HyDe + reranking via Cohere [reddit.com+11reddit.com+11reddit.com+11](https://www.reddit.com/r/Rag/comments/1fu9u5r?utm_source=chatgpt.com).
    

---

### 5. Agentic ou Multi‑Agent RAG

- **Router Agent**: decide a melhor estratégia de recuperação ou rota entre índices, vetores, grafo ou APIs [skphd.medium.com](https://skphd.medium.com/different-rag-architectures-every-ai-professional-should-know-04f228e50fc3?utm_source=chatgpt.com).
    
- **Hierarchical Multi‑Agent RAG (HM‑RAG)**: decomposição de queries, agentes especializados por modalidade e validação via consenso [arxiv.org+15arxiv.org+15skphd.medium.com+15](https://arxiv.org/abs/2504.12330?utm_source=chatgpt.com).
    
- **Multi-Agent RAG Customer Support**: roteamento por auxiliar especializado, com gerenciamento de estado e ferramentas de verificação [github.com](https://github.com/ro-anderson/multi-agent-rag-customer-support?utm_source=chatgpt.com).
    

Trechos da comunidade:

> “Retrieval Becomes Agentic: ... the agent (Router) uses different retrieval tools … decides which tool to invoke based on the context.” [markovate.com+9reddit.com+9skphd.medium.com+9](https://www.reddit.com/r/LangChain/comments/1hzxdgn?utm_source=chatgpt.com)

---

### 6. Query Planning / Adaptive RAG

- **Adaptive RAG**: analisa a complexidade da query e decide dinamicamente se executa um ou múltiplos passos de RAG ou até um caminho sem retrieval [analyticsvidhya.com](https://www.analyticsvidhya.com/blog/2025/01/agentic-rag-system-architectures/?utm_source=chatgpt.com).
    

---

### 7. Graph RAG + Tool Fusion

- **Objetivo**: usar grafo não só para documentos, mas para seleção de ferramentas em agentes (ex: geolocalização, banco SQL) [arxiv.org](https://arxiv.org/html/2502.07223v1?utm_source=chatgpt.com).