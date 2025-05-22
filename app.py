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
def get_todos():
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return todo
        

@api.get('/todos')
def get_all_todos(): 
    return all_todos    

