from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task Management API")


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str


tasks = [
    Task(
        id=1,
        title="Complete Assignment",
        description="Finish FastAPI assignment",
        status="Pending",
        priority="High"
    ),
    Task(
        id=2,
        title="Study Pytest",
        description="Learn testing with pytest",
        status="In Progress",
        priority="Medium"
    )
]


# GET all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# GET single task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# POST create task
@app.post("/tasks", status_code=201)
def create_task(task: Task):

    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists"
            )

    tasks.append(task)

    return task


# PUT update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):
        if task.id == task_id:

            if updated_task.id != task_id:
                raise HTTPException(
                    status_code=400,
                    detail="Task ID mismatch"
                )

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# DELETE task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )