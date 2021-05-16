from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from beans import Task

app = FastAPI()


class TaskJsonItem(BaseModel):
    id: int
    name: str
    content: str


def mock_tasks() -> list[Task]:
    _arr: List[Task] = []
    for i in range(5):
        task = Task(i, f"name{i}", f"content{i}")
        _arr.append(task)
    return _arr


arr = mock_tasks()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/tasks")
def get_tasks():
    return arr


@app.delete("/tasks/{task_id}")
def delete_item(task_id: int):
    _arr = [_item for _item in arr if _item.id == task_id]
    print(f'delete item: {_arr}, len={len(_arr)}')
    for _item in _arr:
        arr.remove(_item)
    return {"success": len(_arr) > 0}


@app.get("/tasks/{task_id}")
def read_item(task_id: int, q: Optional[str] = None):
    return {"item_id": task_id, "q": q}
