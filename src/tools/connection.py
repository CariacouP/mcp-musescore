"""Connection and utility tools for MuseScore MCP."""

from typing import Any, Dict
from ..client import MuseScoreClient
from ..utils.response_formatter import run_and_format_response


def setup_connection_tools(mcp: Any, client: MuseScoreClient) -> None:
    """Setup connection and utility tools."""
    
    @mcp.tool()
    async def connect_to_musescore() -> Dict[str, bool]:
        """Connect to the MuseScore WebSocket API."""
        result = await client.connect()
        return {"success": result}

    @mcp.tool()
    async def ping_musescore() -> Any:
        """Ping the MuseScore WebSocket API to check connection."""
        return await run_and_format_response(client, "ping")

    @mcp.tool()
    async def get_score() -> Any:
        """Get information about the current score."""
        return await run_and_format_response(client, "getScore")