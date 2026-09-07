import asyncio
import json
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.client import MuseScoreClient

async def main():
    client = MuseScoreClient()
    response = await client.send_command("getScore")
    target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "fixtures", "score_dump.json"))
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)
    print(f"Done dumping score to {target_path}")

if __name__ == "__main__":
    asyncio.run(main())
