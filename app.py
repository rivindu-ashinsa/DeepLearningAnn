from fastapi import FastAPI, HTTPException
from typing import Optional, List
from enum import IntEnum
from pydantic import BaseModel, Field



class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=32, description="The name of the todo item")   
    todo_description: str = Field(..., min_length=3, max_length=512, description="The description of the todo item")
    priority: Priority = Field(default=Priority.LOW, description="The priority of the todo item")


class Todo(TodoBase):
    todo_id: int = Field(..., description="The unique identifier of the todo")
class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=32, description="The name of the todo item")   
    todo_description: Optional[str] = Field(None, min_length=3, max_length=512, description="The description of the todo item")
    priority: Optional[Priority] = Field(None, description="The priority of the todo item")


api = FastAPI()

all_todos = [
    Todo(todo_id=1, todo_name='meditate', todo_description='meditate for 10 minutes', priority=Priority.LOW),
    Todo(todo_id=2, todo_name='shopping', todo_description='Go shopping', priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name='sports', todo_description='go the gym', priority=Priority.LOW),
    Todo(todo_id=4, todo_name='study', todo_description='Do the homework', priority=Priority.HIGH),
]


@api.get('/todos/{todo_id}', response_model=Todo)
def get_todos(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
        

@api.get('/todos',response_model=List[Todo])
def get_all_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos    


@api.post('/todos', response_model=Todo)
def create_todo(new_todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id=new_todo_id, todo_description=new_todo.todo_description, todo_name=new_todo.todo_name, priority=new_todo.priority)

    all_todos.append(new_todo)
    return new_todo


@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name
            todo.todo_description = updated_todo.todo_description
            todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail='Todo not found')

@api.delete('/todo/{todo_id}', response_model=Todo)  
def delete_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            all_todos.remove(todo)
            return {'message': 'Todo deleted'}
    raise HTTPException(status_code=404, detail='Todo not found')