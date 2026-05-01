# mad-mcp

Local FastMCP server for controlling Home Assistant lights.

## What it does

- Exposes an MCP tool named `toggle_device(device_id, state)`
- Exposes an MCP prompt named `tool_description`
- Uses Home Assistant REST API service calls to turn lights on or off

## Requirements

- Python 3.14+
- A running Home Assistant instance
- A Home Assistant long-lived access token

## Environment variables

Create a `.env` file with:

```env
assistant_url=http://YOUR_HOME_ASSISTANT_HOST:8123
token=YOUR_LONG_LIVED_ACCESS_TOKEN
```

Notes:

- `assistant_url` is used as the API base URL.
- `token` is sent as a Bearer token in the `Authorization` header.

## Install

This project uses `pyproject.toml`.

```bash
uv sync
```

## Run

Start the MCP server:

```bash
uv run main.py
```

Current server bind from code:

- Host: `0.0.0.0`
- Port: `9000`
- MCP URL path: `/mcp`

So clients should connect to:

`http://localhost:9000/mcp`

## VS Code MCP config

Expected config in `.vscode/mcp.json`:

```json
{
   "servers": {
      "mad-mcp": {
         "type": "http",
         "url": "http://localhost:9000/mcp"
      }
   }
}
```

## Exposed MCP interfaces

### Tool: `toggle_device`

Parameters:

- `device_id` (string), for example `light.80`
- `state` (string): `on` or `off`

Returns:

- `true` on success, `false` on failure

### Prompt: `tool_description`

A reusable server prompt instructing clients to use the tool-first workflow.

## Home Assistant endpoints used

- `GET /api/states` in `get_devices()` (filters to `light.*`)
- `POST /api/services/light/turn_on` or `turn_off` in `toggle_state()`

## Quick checks

Run connector module directly:

```bash
uv run ha_connector.py
```

Run type checks (as currently used in this repo):

```bash
uv run ty check .
```

