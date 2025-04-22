from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to your todo list."}

@app.get("/todo", tags=["todos"])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return {"data": todos}

@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict, db: Session = Depends(get_db)):
    new_todo = models.Todo(item=todo["item"])
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"data": f"Todo '{new_todo.item}' added."}

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.item = body["item"]
    db.commit()
    return {"data": f"Todo with id {id} has been updated."}

@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"data": f"Todo with id {id} has been removed."}
