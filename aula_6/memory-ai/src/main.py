from cli.app import CLIApp
from ai.agent import build_graph

memory = None
agent = build_graph()
app = CLIApp(agent)
if __name__ == "__main__":
    app.run()