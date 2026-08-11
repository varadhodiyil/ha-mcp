"""Home Assistant Connector."""

import asyncio
import http
from enum import StrEnum

import aiohttp
from decouple import config
from dotenv import load_dotenv

load_dotenv()


class DeviceState(StrEnum):
    """Enum for device states."""

    ON = "on"
    OFF = "off"


def init_session() -> aiohttp.ClientSession:
    """Initialize an aiohttp session with the Home Assistant URL and token."""
    url = config("assistant_url")
    return aiohttp.ClientSession(
        url,
        headers={
            "Authorization": f"Bearer {config('token')}",
            "content-type": "application/json",
        },
    )


async def get_devices() -> list[str]:
    """Get a list of devices from Home Assistant."""
    async with init_session() as session:
        response = await session.get("/api/states")
        data = await response.json()

        return [
            device["entity_id"]
            for device in data
            if device["entity_id"].startswith("light.")
        ]


async def toggle_state(device_id: str, state: DeviceState) -> bool:
    """Toggle the state of a device in Home Assistant."""
    async with init_session() as session:
        service = "turn_on" if state == DeviceState.ON else "turn_off"
        response = await session.post(
            f"/api/services/light/{service}",
            json={"entity_id": device_id},
        )
        return response.status == http.HTTPStatus.OK


async def main() -> None:
    """Entry point for testing."""
    await get_devices()
    await toggle_state("light.80", DeviceState.OFF)


if __name__ == "__main__":
    asyncio.run(main())
