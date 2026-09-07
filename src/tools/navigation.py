"""Cursor and navigation tools for MuseScore MCP."""

from typing import Any
from ..client import MuseScoreClient
from ..utils.response_formatter import run_and_format_response


def setup_navigation_tools(mcp: Any, client: MuseScoreClient) -> None:
    """Setup cursor and navigation tools."""

    @mcp.tool()
    async def get_cursor_info() -> Any:
        """Get information about the current cursor position."""
        return await run_and_format_response(client, "getCursorInfo", {"verbose": False})

    @mcp.tool()
    async def go_to_measure(measure: int) -> Any:
        """Navigate to a specific measure."""
        return await run_and_format_response(client, "goToMeasure", {"measure": measure})

    @mcp.tool()
    async def go_to_final_measure() -> Any:
        """Navigate to the final measure of the score."""
        return await run_and_format_response(client, "goToFinalMeasure")

    @mcp.tool()
    async def go_to_beginning_of_score() -> Any:
        """Navigate to the beginning of the score."""
        return await run_and_format_response(client, "goToBeginningOfScore", {"verbose": False})

    @mcp.tool()
    async def next_element() -> Any:
        """Move cursor to the next element."""
        return await run_and_format_response(client, "nextElement")

    @mcp.tool()
    async def prev_element() -> Any:
        """Move cursor to the previous element."""
        return await run_and_format_response(client, "prevElement")

    @mcp.tool()
    async def next_staff() -> Any:
        """Move cursor to the next staff."""
        return await run_and_format_response(client, "nextStaff")

    @mcp.tool()
    async def prev_staff() -> Any:
        """Move cursor to the previous staff."""
        return await run_and_format_response(client, "prevStaff")

    @mcp.tool()
    async def select_current_measure() -> Any:
        """Select the current measure."""
        return await run_and_format_response(client, "selectCurrentMeasure")
        
    @mcp.tool()
    async def select_custom_range(start_tick: int, end_tick: int, start_staff: int, end_staff: int) -> Any:
        """
        Select a custom range of ticks across staves.
        This provides high surgical precision for retrieving continuous phrasing that spans measure bounds.
        """
        params = {
            "startTick": start_tick,
            "endTick": end_tick,
            "startStaff": start_staff,
            "endStaff": end_staff
        }
        return await run_and_format_response(client, "selectCustomRange", params)