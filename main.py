"""Main entry point for the Home Assistant Connector MCP server."""

from fastmcp import FastMCP

from ha_connector import DeviceState, get_devices, toggle_state

mcp = FastMCP(
    "HA Connector",
    "A tool to connect to Home Assistant and toggle device states",
)


@mcp.prompt(name="tool_description")
async def tool_description() -> str:
    """Reusable prompt that asks clients to call toggle_device first."""
    return (
        "Use local MCP tools first. If device_id and state are provided, call "
        "mad-mcp.toggle_device immediately. Return the exact arguments used, "
        "the raw tool result, and a one-line success/failure status. "
        "Valid states: on, off. Retry once after trimming whitespace if a call "
        "fails due to argument formatting. Normalize IDs to Home Assistant "
        "light entities: if device_id does not start with light., prefix it "
        "with light. (example: 80 -> light.80). "
        "Available devices: " + ", ".join(await get_devices())
    )


@mcp.tool(description="Toggle the state of a device in Home Assistant")
async def toggle_device(device_id: str, state: DeviceState) -> bool:
    """Toggle the state of a device in Home Assistant."""
    return await toggle_state(device_id, DeviceState(state))


if __name__ == "__main__":
    mcp.run(transport="http", port=9000, host="0.0.0.0")  # noqa: S104


app = mcp.http_app()
