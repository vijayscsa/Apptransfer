import asyncio
import websockets
import requests
import json
import uuid
import yaml
from dotenv import load_dotenv
import os

class MCPClient:
    def __init__(self, config_path="config.yaml"):
        load_dotenv()
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.server_url = cfg["mcp"]["server_url"]
        self.ws_url = cfg["mcp"]["ws_url"]
        self.api_key = cfg["mcp"]["api_key"]

        self.llm_api_key = os.getenv(cfg["llm"]["api_key_env"], "")

        self.session_id = str(uuid.uuid4())

    async def send_ws(self, message):
        async with websockets.connect(self.ws_url) as ws:
            await ws.send(json.dumps(message))
            response = await ws.recv()
            return json.loads(response)

    async def call_mcp(self, user_message):
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "chat.completion",
            "params": {
                "session_id": self.session_id,
                "message": user_message,
                "llm_api_key": self.llm_api_key
            }
        }
        return await self.send_ws(payload)
