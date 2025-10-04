from fastmcp import FastMCP
import requests

# Inicializa o servidor MCP
mcp = FastMCP("PokemonApi")

BASE_URL = "https://pokeapi.co/api/v2"

# Função auxiliar para requisições

def fetch_from_pokeapi(endpoint: str, params: dict = None):
    url = f"{BASE_URL}/{endpoint.strip('/')}"
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Request failed with status {response.status_code}"}

# Endpoint: Buscar Pokémon por nome ou ID
@mcp.tool()
def get_pokemon(name_or_id: str):
    """Busca detalhes de um Pokémon pelo nome ou ID."""
    data = fetch_from_pokeapi(f"pokemon/{name_or_id}")
    if "error" in data:
        return data

    # Monta resposta limpa
    summary = {
        "id": data["id"],
        "name": data["name"].capitalize(),
        "types": [t["type"]["name"] for t in data["types"]],
        "abilities": [a["ability"]["name"] for a in data["abilities"]],
    }
    return summary

# Endpoint: Listar Pokémons (com paginação)
# @mcp.tool()
# def list_pokemons(limit: int = 20, offset: int = 0):
#     """Lista Pokémons disponíveis com paginação."""
#     return fetch_from_pokeapi("pokemon", {"limit": limit, "offset": offset})

# Endpoint: Buscar tipo de Pokémon
@mcp.tool()
def get_type(name_or_id: str):
    """Busca informações de um tipo de Pokémon."""
    data = fetch_from_pokeapi(f"type/{name_or_id}")
    if "error" in data:
        return data

    damage_relations = data.get("damage_relations", {})
    summary = {
        "id": data["id"],
        "name": data["name"].capitalize(),
        "damage_relations": {
            "double_damage_from": [t["name"] for t in damage_relations.get("double_damage_from", [])],
            "double_damage_to": [t["name"] for t in damage_relations.get("double_damage_to", [])],
            "half_damage_from": [t["name"] for t in damage_relations.get("half_damage_from", [])],
            "half_damage_to": [t["name"] for t in damage_relations.get("half_damage_to", [])],
            "no_damage_from": [t["name"] for t in damage_relations.get("no_damage_from", [])],
            "no_damage_to": [t["name"] for t in damage_relations.get("no_damage_to", [])],
        },
    }

    # Opcional: limitar a lista de Pokémon só para exemplos
    pokemons = data.get("pokemon", [])
    summary["sample_pokemons"] = [p["pokemon"]["name"] for p in pokemons[:5]]

    return summary

# Endpoint: Buscar habilidade
@mcp.tool()
def get_ability(name_or_id: str):
    """Busca informações resumidas de uma habilidade de Pokémon (nome, efeito e exemplos)."""
    data = fetch_from_pokeapi(f"ability/{name_or_id}")
    if "error" in data:
        return data

    # Pega a descrição curta em inglês
    effect_entries = data.get("effect_entries", [])
    effect = next(
        (entry["short_effect"] for entry in effect_entries if entry["language"]["name"] == "en"),
        None,
    )

    summary = {
        "id": data["id"],
        "name": data["name"].replace("-", " ").capitalize(),
        "effect": effect or "No description available",
    }

    # Opcional: limitar Pokémon só para exemplos
    pokemons = data.get("pokemon", [])
    summary["sample_pokemons"] = [p["pokemon"]["name"] for p in pokemons[:5]]

    return summary

if __name__ == "__main__":
    mcp.run(transport="stdio")