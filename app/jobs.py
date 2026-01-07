import asyncio, uuid, os
from dataclasses import dataclass
from typing import Dict, Optional
from .config import settings
from .suno_client import SunoClient

@dataclass
class Job:
    id: str
    task: asyncio.Task
    file: Optional[str] = None
    cancelled: bool = False

jobs: Dict[int, Job] = {}

def cancel(user_id: int):
    job = jobs.get(user_id)
    if job:
        job.cancelled = True
        job.task.cancel()

async def run_job(user_id: int, prompt: str):
    os.makedirs(settings.results_dir, exist_ok=True)
    client = SunoClient(settings.sunoapi_key, settings.sunoapi_base)

    task_id = await client.generate(prompt)
    url = await client.wait_mp3(task_id)

    out = f"{settings.results_dir}/{user_id}_{uuid.uuid4().hex}.mp3"
    await client.download(url, out)
    return out
