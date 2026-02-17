import json

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from chroma_db_adapter import ChromaDB

load_dotenv()

mcp = FastMCP("browser-history", host="0.0.0.0", port=8001)
db = ChromaDB(top_k=2)


@mcp.tool()
def search(query: str) -> str:
    """Search the user's browser history for relevant information. Uses semantic search over previously visited and indexed web pages. Use this tool whenever the user asks a question that could be answered by content they have previously browsed, such as articles, documentation, tutorials, or any other web content. Returns matching text passages with source URLs and page titles."""
    results = db.semantic_search(query)
    return json.dumps([r.model_dump() for r in results], indent=2)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
