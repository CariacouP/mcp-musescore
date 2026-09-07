"""Sequence processing tools for MuseScore MCP."""

from typing import Any
from ..client import MuseScoreClient
from ..types import ActionSequence
from ..utils.response_formatter import run_and_format_response


def setup_sequence_tools(mcp: Any, client: MuseScoreClient) -> None:
    """Setup sequence processing tools."""
    
    @mcp.tool()
    async def processSequence(sequence: ActionSequence) -> Any:
        """Process a sequence of commands."""
        return await run_and_format_response(client, "processSequence", {"sequence": sequence})