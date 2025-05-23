from fastapi import FastAPI

api = FastAPI()

all_todos = [
    {'todo_id' : 1, 'todo_name': 'meditate', 'todo_description': 'meditate for 10 minutes'},
    {'todo_id' : 2, 'todo_name': 'shopping', 'todo_description': 'Go shopping'},
    {'todo_id' : 3, 'todo_name': 'sports', 'todo_description': 'go the gym'},
    {'todo_id' : 4, 'todo_name': 'study', 'todo_description': 'Do the homework'},

]
@api.get('/')
def root():
    return {'message': 'Hello World!'}  


@api.get('/todos/{todo_id}')
def get_todos(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return todo
        

@api.get('/todos')
def get_all_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos    


@api.post('/todos')
def create_todo(new_todo: dict):
    new_todo['todo_id'] = len(all_todos) + 1
    all_todos.append(new_todo)
    return new_todo


@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            todo.update(updated_todo)
            return todo
    return {'message': 'Todo not found'}


@api.delete('/todo/{todo_id}')  
def delete_todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            all_todos.remove(todo)
            return {'message': 'Todo deleted'}
    return {'message': 'Todo not found'}