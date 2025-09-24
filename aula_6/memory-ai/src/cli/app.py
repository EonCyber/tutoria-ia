from ai.agent import extract_ai_answer, input_with_state

class CLIApp:
    def __init__(self, agent):
        self.agent = agent
        self.running = True

    def process_input(self, user_input: str):
        messages = input_with_state(user_input)
        final_state = self.agent.invoke(messages, { "configurable": {"thread_id": "user-1"}})
        answer = extract_ai_answer(final_state)
        return answer

    def run(self):
        while self.running:
            user_input = input("> ")
            if user_input.lower() == "exit":
                self.running = False
                print("Saindo do assistente.")
            else: 
                output = self.process_input(user_input)
                print(f"{output}\n")