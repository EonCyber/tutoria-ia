from fastmcp import FastMCP
import requests
mcp = FastMCP("HumanAsTool")


BASE_URL = "http://localhost:8000"

def fetch_from_mcp(message: str):
    """
    Envia a mensagem para o endpoint /ask e retorna o JSON com reply e message_id.
    """
    url = f"{BASE_URL}/ask"
    try:
        response = requests.post(url, json={"message": message}, timeout=120)
        response.raise_for_status()
        return response.json()  # {'reply': ..., 'message_id': ...}
    except requests.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
# Tool exposta via FastMCP
@mcp.tool()
async def ask_signature_chat(question: str) -> str:
    """
    Use esta ferramenta quando o assistente precisar de **assinaturas de contrato personalizadas** 
    para perguntar diretamente para o humano enviar sua assinatura digital (que será um Hash).

    Parâmetros:
    - question (str): Uma Solicitação feita ao humanao para gerar sua assinatura e devolver na resposta da chamada

    O fluxo esperado:
    1. O assistente identifica a necessidade de intervenção humana.
    2. Chama esta ferramenta com a questão a ser confirmada.
    3. O humano responde , e a resposta é retornada ao assistente.
    """
    # LOGICA AQUI
    data = fetch_from_mcp(question)
    if "error" in data:
        return data
    
    return data.get("reply", "Sem Resposta")

if __name__ == "__main__":
    mcp.run()