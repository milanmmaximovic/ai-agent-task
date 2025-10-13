from fastapi import FastAPI, HTTPException, Path, Body, Response
from typing import Optional, Literal, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import uuid4
from uuid import UUID

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# ---- MODELS ----
Priority = Literal["low", "medium", "high"]
Status = Literal["pending", "completed"]

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[Priority] = "medium"
    due_date: datetime

class TaskOut(TaskIn):
    id: str
    status: Status = "pending"

class StatusUpdate(BaseModel):
    status: Status  # "pending" or "completed"

# ---- IN-MEMORY STORE ----
STORE: dict[str, TaskOut] = {}

# ---- VALIDATION ----
def ensure_due_not_past(d: datetime):
    now = datetime.now(timezone.utc)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    if d < now:
        raise HTTPException(status_code=400, detail="due_date cannot be in the past")

# ---- ROUTES ----
@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn):
    ensure_due_not_past(task.due_date)

    new_task = TaskOut(
        id=str(uuid4()),
        title=task.title,
        description=task.description,
        priority=task.priority or "medium",
        due_date=task.due_date,
        status="pending",
    )
    STORE[new_task.id] = new_task
    return new_task

@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(status: Optional[Status] = None, priority: Optional[Priority] = None):
    result: list[TaskOut] = []

    for t in STORE.values():

        if status is not None and t.status != status:
            continue

        if priority is not None and t.priority != priority:
            continue

        result.append(t)

    return result

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task_by_id(task_id: UUID = Path(..., description="Task ID (UUID)")):
    task = STORE.get(str(task_id))  # keys in the store are saved as strings
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str = Path(..., description="Task ID"),
    data: TaskIn = Body(...)
):
    # 1) find existing task
    existing = STORE.get(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2) validate due_date (not in the past)
    ensure_due_not_past(data.due_date)

    # 3) prepare new object (PUT = full replacement),
    #    but keep the status unchanged (modified via PATCH)
    updated = TaskOut(
        id=task_id,
        title=data.title,
        description=data.description,
        priority=data.priority or "medium",
        due_date=data.due_date,
        status=existing.status,   # status remains unchanged in PUT
    )

    # 4) save to store
    STORE[task_id] = updated

    # 5) return result
    return updated

@app.patch("/tasks/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: str = Path(..., description="Task ID"),
    payload: StatusUpdate = Body(...)
):
    # 1) find existing task
    existing = STORE.get(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2) change status (enum validation handled by Pydantic)
    existing.status = payload.status

    # 3) save back and return
    STORE[task_id] = existing
    return existing

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str = Path(..., description="Task ID")):
    # 1) if not found → 404
    if task_id not in STORE:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2) remove and return 204 without body
    STORE.pop(task_id, None)
    return Response(status_code=204)
