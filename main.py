
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Todo
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
def add_todo(title: str = Form(...), db: Session = Depends(get_db)):
    todo = Todo(title=title)
    db.add(todo)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.delete("/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message": "Deleted"}
    return {"error": "Not found"}

class EditTodo(BaseModel):
    title: str

@app.put("/edit/{todo_id}")
def edit_todo(todo_id: int, item: EditTodo, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.title = item.title
        db.commit()
        return {"message": "Updated"}
    return {"error": "Not found"}
