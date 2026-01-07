import asyncio
import httpx

class SunoClient:
    def __init__(self, api_key: str, base: str):
        self.api_key = api_key
        self.base = base.rstrip("/")

    def headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    async def generate(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                f"{self.base}/api/v1/generate",
                json={
                    "prompt": prompt,
                    "customMode": False,
                    "instrumental": False,
                    "model": "V4_5ALL",
                },
                headers=self.headers(),
            )
            r.raise_for_status()
            return r.json()["data"]["taskId"]

    async def wait_mp3(self, task_id: str) -> str:
        async with httpx.AsyncClient(timeout=60) as c:
            while True:
                r = await c.get(
                    f"{self.base}/api/v1/generate/record-info",
                    params={"taskId": task_id},
                    headers=self.headers(),
                )
                r.raise_for_status()
                data = r.json()["data"]
                if data["status"] == "SUCCESS":
                    return data["response"]["sunoData"][0]["audioUrl"]
                await asyncio.sleep(3)

    async def download(self, url: str, path: str):
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.get(url)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
