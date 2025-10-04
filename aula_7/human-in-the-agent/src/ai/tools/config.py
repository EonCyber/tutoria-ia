# MCP_SERVERS_CONFIG = {
#     "PokemonApi": {
#         "command": "python",
#         "args": ["src/ai/tools/poke_mcp.py"],
#         "transport": "stdio"
#     }
# }

MCP_SERVERS_CONFIG = {
    "PokemonApi": {
        "command": "python",
        "args": ["src/ai/tools/poke_mcp.py"],
        "transport": "stdio"
    },
    "HumanAsTool": {
        "command": "python",
        "args": ["src/ai/tools/signature_human_mcp.py"],
        "transport": "stdio"
    }
}

