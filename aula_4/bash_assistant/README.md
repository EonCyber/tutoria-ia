Perguntas para Agente Bash Assistant

1. "Como mostrar arquivos ocultos no terminal?"
Esperado: ls -a

RAG simples pode retornar ls, ls -l, ls -h

Reranker prioriza ls -a por "ocultos"

2. "Como buscar por uma palavra em vários arquivos?"
Esperado: grep -r ou grep com exemplos recursivos

RAG simples pode trazer só grep genérico

Reranker destaca exemplos com -r ou --include

3. "Como ver o uso de memória da máquina?"
Pode ser free, top, htop, vmstat

RAG simples retorna o primeiro que "bate"

Reranker pode escolher free com explicação de MB

4. "Como criar uma pasta?"
Esperado: mkdir

RAG simples pode misturar com touch, cp

Reranker tende a priorizar exemplo direto de mkdir

5. "Como apagar uma pasta que não está vazia?"
Esperado: rm -r ou rm -rf

RAG simples pode sugerir rm sem contexto

Reranker prioriza o com -r

6. "Como copiar uma pasta inteira com arquivos?"
Esperado: cp -r

RAG simples pode mostrar cp comum

Reranker encontra cp -r com descrição completa

7. "Como ver os últimos comandos executados?"
Esperado: history, fc, ! etc

RAG simples pode trazer comandos genéricos

Reranker deve dar prioridade a history

8. "Como verificar o status de um serviço no sistema?"
Esperado: systemctl status <serviço>

RAG simples pode trazer qualquer comando com "status"

Reranker deve priorizar systemctl

9. "Como contar o número de linhas de um arquivo?"
Esperado: wc -l

RAG simples pode trazer cat, less, etc.

Reranker deve elevar wc -l

10. "Como mover um arquivo de um diretório para outro?"
Esperado: mv origem destino

RAG simples pode misturar com cp ou rsync

Reranker destaca mv com exemplos claros