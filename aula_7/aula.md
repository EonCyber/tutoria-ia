
# Função do Humano em Sistemas de IA
#agentes #aula #mentoriafire #genai #humanintheloop


### 1. **Cibernética e Controle de Sistemas**

- Na **cibernética** (Norbert Wiener, anos 1940), sistemas complexos são modelados como ciclos de **entrada → processamento → saída → feedback**.
    
- O _loop de feedback_ é o ponto onde o sistema ajusta seu comportamento com base nos resultados.

### 2. **Teoria de Sistemas Sociotécnicos**

- Nos anos 1950-60, a escola de **sistemas sociotécnicos** (Trist & Emery) mostrou que **nenhum sistema técnico funciona isolado**: ele precisa considerar o papel humano.
    
- O humano não é apenas "supervisor", mas parte essencial da **otimização global** (tecnologia + pessoas).
    
- Essa visão explica porque deixar tudo 100% automatizado pode levar a falhas graves de aceitação, usabilidade ou ética.

### 3. **Controle Adaptativo e Supervisão**

- Em **engenharia de controle**, existe o conceito de **controle adaptativo supervisionado**:
    
    - A máquina executa o controle normal.
        
    - Se a situação sair dos limites esperados (incerteza, erro alto, anomalia), o humano é chamado para assumir o loop.

### 4. **Teoria da Decisão e Risco**

A teoria da decisão e risco vem da interseção de:

- **Economia (utilidade esperada, 1944)**.
    
- **Estatística (probabilidade e inferência, redes bayesianas, 1763 - 1950)**.
    
- **Psicologia (heurísticas e vieses cognitivos, 1970: Herbert Simon)**.
    
- **Engenharia (aplicação prática em sistemas complexos e risco operacional)**.

Resumidamente:
- O **custo do erro** é alto.
    
- O **grau de incerteza** do modelo é grande.
    
- A decisão exige **valores éticos ou contexto social** que não podem ser codificados facilmente.
  
Então a intervençao na decisão deve ser feita por uma pessoa capacitada.


## Human-in-the-Loop

Apesar do conceito começar a ser utilizado nos anos 90 e 2000 para inteligencia artificial, principalmente no quesito de rotulaçao de dados de treinamento e feedback nos outputs.

O termo ganha nova vida em 2017 e 2018, com o boom dos modelos de linguagem (transformers de nlp)

Em 2019-2020 a Open Ai causa a popularização do termo com o uso de Reinforcement Learning from Human Feedback (RLHF) (a avaliaçao de output dos modleos de linguagem para treinamentos melhores)

## AI Engineering

- **Human-in-the-Loop (HITL)** é a prática de incluir **intervenção, feedback e supervisão humana** dentro do ciclo de desenvolvimento, operação e tomada de decisão de sistemas de IA.
    
- Na **AI Engineering moderna**, HITL não é só supervisão, mas um **componente arquitetural** do sistema: parte do design de agentes inteligentes, pipelines de ML/LLM e governança.

HITL vai ser utilizado como boa prática de desenvolvimento e como forma de aumentar o Score de confiabilidade de respostas de um sistema com Gen IA.

Tratando alucinações, confirmando decisões e provendo novas informações através da intervenção humana.

Quanto mais crítico as decisoes que um agente pode tomar, mais se torna importante o uso de HITL para esse sistema.

Isso deve melhorar:
- A Governança do Sistema.
- Feedbacks para melhoria continua.
- Fallback para casos ambíguos.

### **Benefícios**

- **Segurança**: evita erros graves e outputs tóxicos.
    
- **Confiança**: usuários aceitam mais um sistema quando sabem que tem humano envolvido.
    
- **Aprendizado Contínuo**: humanos ajudam o sistema a melhorar ao longo do tempo.
    
- **Flexibilidade**: humanos cobrem lacunas que o modelo sozinho não consegue preencher.

> No AI Engineering moderno, Human-in-the-Loop não é só supervisionamento é design de agentes e sistemas onde o humano é parte ativa do ciclo de decisão, atuando como guardrail, treinador e colaborador.


### Componentes no LangGraph

**Interrupt** -> Função usada para parar a execução de um node do grafo quando se quer envolvimento humano.
**Command(resume=)** -> Comando usado para retornar a execução do Grafo após a interrupção, injetando a resposta humana.
**Checkpointing** -> Salva o estado do grafo ao longo da execução, é usado para poder retornar para aquele ponto na sessão após um interrupt(). (Memory)


## O que caracteriza “Human as a Tool”

- O humano não apenas supervisiona ou corrige (como em HITL), mas é chamado como “módulo funcional” quando necessário para tarefas que o agente não consegue ou não deve executar.
    
- Serve para preencher lacunas, fazer julgamentos de valor, prover contexto humano, ou executar tarefas que exigem habilidades humanas específicas.
    
- Geralmente usado em fluxos híbridos, agentes cooperativos ou sistemas colaboradores.


**Human as a Tool** é essencial quando o agente **não consegue produzir sozinho** e depende do humano como parte funcional do pipeline, enquanto o HITL é apenas **corretivo ou de supervisão**.

É uma boa prática na criação de Agentes/Assistentes e Sistemas que tomem decisões.


# Casos De Uso da Aula

assinatura digital
orçamento critico
autenticacao manual