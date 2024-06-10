import os
from flask import Flask, request, render_template, jsonify
from prisma import Prisma
import google.generativeai as genai
import marko
from tools.tools import get_todos, add_todo, update_todo, delete_todo, find_todo_by_title_or_description

# Initialize Prisma client
db = Prisma()
db.connect()

genai.configure(api_key=os.getenv("API_KEY"))
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    todos = db.todo.find_many()
    return render_template("index.html", todos=todos)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_todos, add_todo, update_todo, delete_todo, find_todo_by_title_or_description],
)

model_chat = model.start_chat(enable_automatic_function_calling=True)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == "GET":
        return render_template("chat.html")
    else:
        data = request.json
        message = data["message"]
        response = model_chat.send_message(message)
        print("Message: ", message)
        print("Response: ", response.text)
        return jsonify({"response": marko.convert(response.text)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
