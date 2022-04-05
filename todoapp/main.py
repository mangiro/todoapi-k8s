from typing import List

from fastapi_sqlalchemy import db
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI, Response, HTTPException

from .models import Task
from .db import metadata, engine
from .schemas import TaskCreate, TaskUpdate, TaskObj

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url="sqlite:///./tasks.db")


@app.on_event('startup')
async def startup_event():
    metadata.create_all(engine)


@app.get("/tasks", status_code=200, response_model=List[TaskObj])
def get_tasks():
    with db():
        tasks = db.session.query(Task).all()

    return tasks


@app.get("/tasks/{task_id}", status_code=200, response_model=TaskObj)
def get_task_by_id(task_id: int):
    with db():
        task = db.session.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found."
        )

    return task


@app.post("/tasks", status_code=201, response_model=TaskObj)
def create_task(task_in: TaskCreate):
    with db():
        obj_in_data = jsonable_encoder(task_in)
        db_obj = Task(**obj_in_data)  # type: ignore

        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)

    return db_obj


@app.patch("/tasks/{task_id}", status_code=200, response_model=TaskObj)
def update_task(task_id: int, task_in: TaskUpdate):
    with db():
        task = db.session.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found."
            )

        db_task = jsonable_encoder(task)

        if isinstance(task_in, dict):
            update_data = task_in
        else:
            update_data = task_in.dict(exclude_unset=True)

        for field in db_task:
            if field in update_data:
                setattr(task, field, update_data[field])

        db.session.add(task)
        db.session.commit()
        db.session.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with db():
        task = db.session.query(Task).filter(Task.id == task_id).first()

        if not task:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found."
            )

        db.session.delete(task)
        db.session.commit()

    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
