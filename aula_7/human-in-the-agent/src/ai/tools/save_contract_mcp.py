from fastmcp import FastMCP
import os
from datetime import datetime
import re
from typing import Optional

mcp = FastMCP("ContractGenerator")

CONTRACTS_DIR = "./contracts"
os.makedirs(CONTRACTS_DIR, exist_ok=True)

def _sanitize_filename(name: str) -> str:
    # Remove caracteres que dão problema em filenames e deixa só letras, números, -, _
    name = name.strip()
    # substitui espaços por _
    name = re.sub(r"\s+", "_", name)
    # remove chars indesejados
    name = re.sub(r"[^A-Za-z0-9_\-\.]", "", name)
    return name or "contract"

def _timestamp_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

@mcp.tool()
def generate_md_contract(content: str, filename: Optional[str] = None) -> dict:
    """
    Gera um arquivo .md com o conteúdo recebido e salva em ./contracts.
    Args:
      - content: texto em Markdown do contrato
      - filename: nome base para o arquivo (opcional). Se não fornecido, usa 'contract'.
    Returns:
      - dict com keys: success (bool), path (str) ou error (str)
    """
    try:
        base = filename or "contract"
        base_clean = _sanitize_filename(base)
        fname = f"{base_clean}_{_timestamp_str()}.md"
        path = os.path.join(CONTRACTS_DIR, fname)

        # escreve o arquivo
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # roda o MCP no stdio (compatível com MultiServerMCPClient usando transport stdio)
    mcp.run(transport="stdio")
