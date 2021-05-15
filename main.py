from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from beans import Task

app = FastAPI()


class TaskItem(BaseModel):
    id: int
    name: str
    content: str


@app.get("/tasks")
def get_tasks():
    arr: List[Task] = []
    for i in range(5):
        task = Task(i, f"name{i}", f"content{i}")
        arr.append(task)
    return arr


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
