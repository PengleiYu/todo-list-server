import functools
from typing import List, Callable
from fastapi import FastAPI
from pydantic import BaseModel

from beans import Task

app = FastAPI()


class TaskJsonItem(BaseModel):
    name: str
    content: str


def mock_tasks() -> List[Task]:
    _arr: List[Task] = []
    for i in range(5):
        task = Task(i, f"name{i}", f"content{i}")
        _arr.append(task)
    return _arr


def find_item(item_list: List[Task], predictor: Callable[[Task], bool]) -> List[Task]:
    return [_item for _item in item_list if predictor(_item)]


arr = mock_tasks()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/tasks")
def select_task_list():
    return arr


@app.get("/tasks/{task_id}")
def select_task(task_id: int):
    _arr = find_item(arr, lambda it: it.id == task_id)
    if len(_arr) != 0:
        return _arr[0]
    return None


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    _arr = find_item(arr, lambda it: it.id == task_id)
    print(f'delete item: {_arr}, len={len(_arr)}')
    for _item in _arr:
        arr.remove(_item)
    return len(_arr) > 0


@app.put("/tasks/add")
def insert_task(item: TaskJsonItem):
    _next_id = functools.reduce(max, map(lambda it: it.id, arr)) + 1
    _task = Task(_next_id, item.name, item.content)
    arr.append(_task)
    return _next_id


@app.post('/tasks/{task_id}')
def update_task(task_id: int, item: TaskJsonItem):
    print(f'task_id={task_id}, item={item}')
    _arr = find_item(arr, lambda it: it.id == task_id)
    if len(_arr) == 0:
        return -1
    _task = _arr[0]
    _task.name = item.name
    _task.content = item.content
    return _task.id
