from sqlalchemy import Column, Integer, String
from app.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
