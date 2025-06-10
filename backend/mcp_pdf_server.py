from mcp.server.fastmcp import FastMCP
from mcp.types import Resource

mcp = FastMCP("northwind")
#Filler prompt
@mcp.prompt()
def example_prompt(code: str) -> str:
    return f"Please review this code:\n\n{code}"

if __name__ == "__main__":
    print("Starting server...")
    # Initialize and run the server
    mcp.run(transport="stdio")