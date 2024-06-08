import os
from flask import Flask, request, render_template, jsonify
from prisma import Prisma
import google.generativeai as genai
import marko

# Initialize Prisma client
db = Prisma()
db.connect()

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
app.debug = True

model = genai.GenerativeModel(model_name="gemini-pro-vision")

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

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_image' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['user_image']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        image_data = file.read()
        image_parts = [
            {
                "mime_type": file.content_type,
                "data": image_data
            },
        ]

        prompt_parts = [
            "You are Sheldon Cooper. User will upload an image. Based on the image, you have to come up with a Sheldon Cooper style fun fact. Also give a funny, sarcastic note about the image. \n\nUser's image:\n\n",
            image_parts[0],
            "\n\nFun fact:\n",
        ]    

        response = model.generate_content(prompt_parts)

        return jsonify({
            "response": marko.convert(response.text)
        })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
