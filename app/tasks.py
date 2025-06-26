from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    'tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task(name="generate_clips")
def generate_clips(prompt: str, seconds: int, n_clips: int = 3):
    # Placeholder: Replace with actual video generation logic
    return {
        "prompt": prompt,
        "seconds": seconds,
        "n_clips": n_clips,
        "status": "processing"
    } 