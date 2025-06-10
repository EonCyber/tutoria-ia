from keyflow import kfprint
from ai.llm import ChatBot
class CLIApp:
    
    def __init__(self):
        self.running = True
        self.chatbot = ChatBot()
    
    def process_input(self, user_input: str) -> str:
        return self.chatbot.answer(user_input)
    
    def run(self):
        kfprint("Mentoria Fire - Tutoria LLM Aula 1\n", speed = 0.05, fore_color="green", bold= True)
        
        while self.running:
            user_input = input("> ")
            if user_input.lower() == "exit":
                self.running = False
                kfprint("Goodbye!!\n", speed = 0.05, fore_color="green", bold= True)
            else: 
                output = self.process_input(user_input)
                kfprint(f"{output}\n", speed = 0.05, fore_color="green", bold= True)
