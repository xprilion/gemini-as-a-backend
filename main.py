import os
from flask import Flask, request, render_template, jsonify
from prisma import Prisma

# Initialize Prisma client
db = Prisma()
db.connect()

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    todos = db.todo.find_many()
    return render_template("index.html", todos=todos)

@app.route('/todo', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description')

    if title:
        db.todo.create({
            'title': title,
            'description': description,
        })
    return jsonify({"status": "success"})

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    db.todo.delete(where={"id": id})
    return jsonify({"status": "success"})

@app.route('/todo/<id>', methods=['PATCH'])
def update_todo(id):
    is_completed = request.json.get('isCompleted')
    db.todo.update(where={"id": id}, data={"isCompleted": is_completed})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
