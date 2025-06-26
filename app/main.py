from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import app.tasks as tasks

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    seconds: int
    n_clips: int = 3

class RenderRequest(BaseModel):
    clip_id: str
    voice_id: str
    title: str
    prompt: str
    seconds: int

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/clips/generate")
async def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    job = tasks.generate_clips.delay(req.prompt, req.seconds, req.n_clips)
    return {"job_id": job.id}

@app.get("/clips/{job_id}")
async def get_clip_status(job_id: str):
    result = tasks.generate_clips.AsyncResult(job_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    elif result.state == "FAILURE":
        raise HTTPException(status_code=500, detail="Job failed")
    else:
        return {"status": result.state} 