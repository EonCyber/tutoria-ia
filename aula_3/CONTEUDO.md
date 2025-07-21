#genai #langgraph #langchain #agentes #aula #mentoriafire 

## 1. 🌉 Diferença entre LLM Applications (non-agentic) e Agentic LLM Applications

### LLM Application (com Chain, Prompt ou Tool Calling)

- **Determinística / Linear**: recebe um input, processa via um fluxo previsível (ex: prompt → LLM → output).
    
- **Chains**: modelam sequências de passos (ex: perguntar → buscar documento → responder).
    
- **Tool Calling**: LLM chama funções externas sob demanda, com base no input.
    

### Agentes com LLM

- **Autonomia e raciocínio iterativo**: não seguem um fluxo fixo, e sim _decidem_ o que fazer com base no estado atual.
    
- **Tomam decisões**: escolhem ferramentas, reavaliam contexto, planejam passos futuros.
    
- **Têm memória e objetivo**: recebem uma _tarefa_ e a perseguem até completar.
    

🔁 **Exemplo claro**:

- Uma chain pode responder “qual a capital da França?” com um lookup.
    
- Um agente pode receber “organize minha agenda da semana” e interagir com múltiplas ferramentas e decisões até concluir a tarefa.

#### 💰 **Custo e uso de tokens em Agentes vs Aplicações não Agenticas**
### ⚖️ Comparativo geral:

| Aspecto                       | LLM Tradicional (não agente)      | LLM Agent (com raciocínio e ações)               |
| ----------------------------- | --------------------------------- | ------------------------------------------------ |
| 🧾 **Chamadas ao modelo**     | 1 ou poucas por interação         | Múltiplas chamadas por tarefa                    |
| 🧠 **Tokens de entrada**      | Prompt direto + contexto limitado | Prompt + histórico de raciocínio + state         |
| 📤 **Tokens de saída**        | Apenas resposta final             | Várias respostas intermediárias + logs           |
| 🔁 **Iterações**              | Normalmente uma                   | 3, 5, 10+ por tarefa, dependendo da complexidade |
| ⚙️ **Ferramentas externas**   | Raras ou manuais                  | Invocadas frequentemente pelo agente             |
| 💸 **Custo final (estimado)** | Baixo e previsível                | Mais alto e variável (depende da lógica)         |
📌 **Por que agentes consomem mais tokens?**

- **Loop de raciocínio (ReAct)**:
    
    - Cada pensamento + ação + observação é uma nova chamada.
        
    - Ex: "Pensando" → "Ação: Buscar" → "Observação: Resultado" → repete...
        
- **Prompt mais longo**:
    
    - Para cada passo, o prompt inclui histórico de ações anteriores.
        
    - Muitas vezes há uma "memória" temporária com o state completo.
        
- **Tomada de decisão explícita**:
    
    - O LLM precisa ser instruído a escolher entre ferramentas, avaliar condições, ou decidir próximo passo — o que exige mais contexto no input.
#### ✅ Aplicação tradicional:

- Prompt: 500 tokens
    
- Resposta: 300 tokens  
    **Total: ~800 tokens por tarefa**
    

#### 🤖 Agente com 5 ciclos ReAct:

- Prompt inicial: 700 tokens (com ferramentas + instruções)
    
- 5 passos com raciocínio/ação/observação:
    
    - Cada loop: 400~700 tokens
        
- Total: ~3000–5000 tokens por tarefa
    

> **Resultado:** Agentes podem custar **4x a 10x mais tokens** por tarefa comparado a chamadas diretas.

### ⚠️ **Quando isso vale a pena?**

- Quando a **tarefa é complexa**, multietapas ou exige **autonomia**.
    
- Quando o custo humano de intervenção seria mais caro.
    
- Quando **flexibilidade e escalabilidade** são prioridade (ex: copilots, automações, assistentes).
    

---

### 💡 **Boas práticas para reduzir custo de agentes**

- Limitar profundidade de ciclos (`max_iterations` no LangGraph).
    
- Usar `cache` em ferramentas e LLMs.
    
- Minimizar quantidade de tokens no state/contexto.
    
- Criar _short-term memory compression_ (resumir histórico).
    
- Escolher modelos menores onde possível (ex: GPT-3.5 para raciocínio leve, GPT-4 para etapas críticas).

## 2. 🤖 Algoritmos de Agentes de LLM
### 2.1. ReAct (Reason + Act)

- 📚 Paper: _ReAct: Synergizing Reasoning and Acting in Language Models_
    
- 🧠 LLM alterna entre _pensar_ (reasoning) e _agir_ (fazer chamadas de ferramentas).
    
- Exemplo:
    
    - Thought: "Preciso buscar os eventos da agenda"
        
    - Action: `get_calendar_events()`
        

✅ Vantagens: eficaz para tarefas com raciocínio lógico e múltiplas etapas.  
⚠️ Desafio: sem memória de longo prazo nativa.

---
### 2.2. Plan & Execute (Planner + Executor)

- 📅 Divide o problema em duas fases:
    
    - **Planner**: cria um plano de alto nível.
        
    - **Executor**: executa cada etapa do plano com raciocínio local.
        
- Bom para tarefas longas e complexas (ex: planejamento de viagem, pipelines).
    

✅ Vantagens: maior controle e previsibilidade.  
⚠️ Mais complexo de implementar.

---
### 2.3. Conversational Agent

- 🗣️ Mantém um diálogo com o usuário, decide ações com base no histórico.
    
- Usa memória conversacional, tracking de contexto e decisões.
    

✅ Vantagens: ótimo para chatbots e assistentes.  
⚠️ Limitação em tarefas com múltiplos objetivos simultâneos.

--- 
### 2.4. AutoGPT-style Agents (Loop autônomo)

- 🔁 O LLM define o objetivo, pensa, age, reflete e repete o ciclo até o objetivo ser alcançado.
    
- Integra raciocínio, ferramentas e criticidade.
    

✅ Poderosos para exploração aberta.  
⚠️ Dificuldade de controle, alto custo computacional.

--- 
### 2.5. Outros Modelos Relevantes

- **Reflexion**: LLM avalia suas próprias ações, ajustando o comportamento.
    
- **Toolformer**: LLM aprende _quando_ usar ferramentas a partir do treinamento supervisionado.

## 3. 🧠 Multi-Agent Systems e Swarms

### O que é um sistema multiagente?

- Uma arquitetura onde **vários agentes** cooperam, competem ou se comunicam para atingir objetivos.
    
- Cada agente pode ter:
    
    - Um papel distinto (planner, executor, comunicador).
        
    - Autonomia parcial.
        
    - Um objetivo local e/ou global.
        

### Como funciona?

- Pode usar:
    
    - **Coordenação direta**: mensagens entre agentes.
        
    - **Ambientes compartilhados**: ex: blackboards, memória comum.
        
- Estratégias de orquestração:
    
    - Hierárquica (um agente líder)
        
    - Heterárquica (todos iguais)
        
    - Swarm (inspirado em colônias de insetos)
        

### Para que pode ser usado?

- 👷 DevOps (ex: um swarm para deploy)
    
- 📅 Organização pessoal (um agente para agenda, outro para e-mails, outro para tarefas)
    
- 🔬 Pesquisa e raciocínio colaborativo (multiagentes debatendo soluções)
    
- 🧬 Simulação de comportamento coletivo (IA social, jogos, IoT)

## 4. ⚙️ Introdução ao LangGraph

### O que é o LangGraph?

- Um _motor de agentes baseado em grafos de estado_.
    
- Foi criado para dar **controle, segurança e auditabilidade** na execução de agentes.
    
- Inspirado em grafos de automatos finitos.
    

### Componentes principais:

1. **StateGraph**: define os nós e transições possíveis.
    
2. **States**: representam a memória e estado da execução.
    
3. **Edges (Transições)**: controlam o fluxo, com lógica condicional.
    
4. **Node Functions**: ações executadas em cada estado.
    
5. **Checkpoints**: permitem retomar, debugar, versionar execuções.
    
6. **LangGraph Studio**: interface de visualização do fluxo em tempo real.
    

### Benefícios:

- 💡 Fácil visualização do fluxo do agente.
    
- 🔐 Previsibilidade e testes.
    
- 🔁 Suporte a loops, branches e paralelismo.
    
- 🧠 Perfeito para construir sistemas multiagentes e controláveis.


###  Apoio

📌 Tipos Comuns de Nodes:

| Tipo de Node | Função típica                               | Exemplo                            |
| ------------ | ------------------------------------------- | ---------------------------------- |
| `llm`        | Chamadas a LLM para decidir ou gerar saídas | "Decida qual ferramenta usar"      |
| `tool`       | Chamada a ferramenta externa                | `get_events_from_calendar()`       |
| `router`     | Direciona o fluxo com base em condições     | "Se for erro, vá para retry"       |
| `planner`    | Gera uma lista de etapas (Plan & Execute)   | "1. Buscar info; 2. Executar ação" |
| `executor`   | Realiza uma etapa do plano                  | "Buscar info sobre clima"          |
| `final`      | Marca o término do grafo                    | Encerrar a execução com resultado  |
🔸 2. **Edges (Arestas)**

Arestas definem as **transições entre os nodes**. Podem ser:

- **Fixas**: vão sempre do Node A para o Node B.
    
- **Condicionais**: escolhem o próximo node com base no estado.
    
- **Loop**: o node aponta para si mesmo (útil para ciclos como em ReAct ou AutoGPT).
    
- **Parallel branches**: múltiplas transições partindo de um node.
📌 Formas comuns de edges:

|Tipo de Edge|Como é definido|Exemplo|
|---|---|---|
|`.add_edge("A", "B")`|Transição simples|Após o node A, vá para B|
|`.add_conditional_edges("A", condition_fn)`|Escolha baseada em lógica|Se `state["done"] == True`, vá para "final"|
|`.add_loop("A")`|Volta para o mesmo node|Repetição enquanto necessário|
|`.add_branching_edges(...)`|Execução paralela ou múltipla|Em multiagente ou pipelines|
🔸 3. **START e FINAL**

LangGraph define dois nodos especiais:

- `START`: ponto inicial da execução.
    
- `FINAL`: ponto de parada quando a execução termina.

```
graph = StateGraph(...)
graph.set_entry_point("start")
graph.add_edge("start", "llm_decision")
graph.add_edge("llm_decision", "tool_use")
graph.add_edge("tool_use", "FINAL")

```
