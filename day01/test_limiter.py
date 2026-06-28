import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        for i in range(8):
            r = await client.get("http://127.0.0.1:8000/valuation")
            print(f"Request {i+1}: {r.status_code} — {r.json()}")

asyncio.run(test())