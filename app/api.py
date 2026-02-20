import time
from fastapi import APIRouter, HTTPException, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .models import TaskCreate
from .storage import InMemoryTaskStore
from .metrics import REQUESTS_TOTAL, REQUEST_LATENCY

router = APIRouter()
store = InMemoryTaskStore()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/tasks")
def list_tasks():
    return store.list_tasks()


@router.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    return store.create_task(task)


@router.post("/tasks/{task_id}/done")
def mark_done(task_id: int):
    task = store.mark_done(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


