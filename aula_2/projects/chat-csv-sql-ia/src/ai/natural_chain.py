from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
class NaturalChain:

    def __init__(self, prompt, llm, db, sql_chain):
        self.llm = llm
        self.prompt = prompt
        self.db = db
        self.sql_chain = sql_chain

    def chain(self):
        return (
            RunnableMap({
                "schema": RunnableLambda(lambda _: self.db.get_table_info()), # Busca o Schema do Db e Injeta no Prompt <== Optimize???
                "question": itemgetter("question")
            })
            | RunnableMap({  # 1: Gera Query SQL e passa a Pergunta para proxima etapa
                "sql": self.sql_chain,
                "schema": itemgetter("schema"),
                 "question": itemgetter("question")
            })
            | RunnableMap({  # 2: O resultado da chain sera injetado no prompt
                "schema": itemgetter("schema"),
                "sql_response": RunnableLambda(lambda args: self.db.run(args["sql"])), # Roda a Query contra o DB e injeta no Prompt 
                "question": itemgetter("question") # Injeta a question no prompt final
            })
            | self.prompt
            | self.llm
            | StrOutputParser()
        )