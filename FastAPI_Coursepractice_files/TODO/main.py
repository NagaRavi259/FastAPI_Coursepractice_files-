from fastapi import FastAPI , Depends, HTTPException
from sqlalchemy.orm import Session
from models import todos
import models
from DataBase import engine, sessionLocal
from pydantic import BaseModel, Field
from typing import Optional
from auth import get_current_user, get_user_execption

app = FastAPI()
 
models.base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = sessionLocal() # we started a session with local db with sessionlocal  
        yield db
    finally:
        db.close()

class ToDo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="the priority must be between one and five")
    complete: bool


@app.get("/")
async def read_all(db:Session=Depends(get_db)):
    return db.query(models.todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id:int, user:dict = Depends(get_current_user), db:Session=Depends(get_db)):
    if user is None:
        raise get_user_execption()
    todo_model=db.query(models.todos).filter(models.todos.id==todo_id).filter(models.todos.owner_id==user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTP_execption()

@app.post("/")
async def create_todo(todo:ToDo, db:Session=Depends(get_db)):
    todo_model = models.todos()
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()

    return successfll_response(200)

@app.get("/todos/user")
async def read_all_by_user(user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    if user is None:
        raise get_user_execption
    return db.query(models.todos).filter(todos.owner_id==user.get("id")).all()

@app.put("/{todo_id}")
async def update_todo(todo_id:int,todo:ToDo,db:Session=Depends(get_db)):
    todo_model = db.query(todos).filter(todos.id==todo_id).first()

    if todo_model is None:
        raise HTTP_execption()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successfll_response(200)

@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo_model = db.query(todos).filter(todos.id==todo_id).first()
    if todo_model is None:
        raise HTTP_execption()
    db.query(todos).filter(todos.id==todo_id).delete()
    db.commit()
    return successfll_response(200)

def successfll_response(status_code:int):
    return {"status":status_code,
            'transaction':'Successuful'}

def HTTP_execption():
    return HTTPException(status_code=404,detail="Todo not found")