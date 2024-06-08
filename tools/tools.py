from flask import jsonify
from prisma import Prisma


db = Prisma()
db.connect()


def get_todos():
    """
    Retrieves all to-do items from the database.

    Args:

    Returns:
        list of todos: A list of todo dicts
    """
    todos = db.todo.find_many()
    result = []

    for todo in todos:
        print(todo)
        # result.append(todo.dict())
        result.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "isCompleted": todo.isCompleted,
        })
    return result

def add_todo(title: str, description: str):
    """
    Adds a new to-do item to the database.

    Args:
        title (str): The title of the to-do item. (Required)
        description (str): The description of the to-do item. (Required)

    Returns:
        flask.Response: A JSON response indicating the success of the operation.
    """
    if title:
        db.todo.create({
            'title': title,
            'description': description,
        })
    return "Success"

def delete_todo(id: str):
    """
    Deletes an existing to-do item from the database.

    Args:
        id (str): The CUID of the to-do item to delete. (Required)

    Returns:
        flask.Response: A JSON response indicating the success of the operation.
    """
    db.todo.delete(where={"id": id})
    return "Success"

def update_todo(id: str, is_completed: bool):
    """
    Updates the completion status of an existing to-do item in the database.

    Args:
        id (str): The CUID of the to-do item to update. (Required)
        is_completed (bool): The new completion status of the to-do item. (Required)

    Returns:
        flask.Response: A JSON response indicating the success of the operation.
    """
    db.todo.update(where={"id": id}, data={"isCompleted": is_completed})
    return "Success"
