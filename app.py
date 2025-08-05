from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

app = Flask(__name__)

# Mongo config
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise RuntimeError("MONGO_URI missing in .env")
client = MongoClient(mongo_uri)
db = client[os.getenv("DB_NAME", "mydb")]
collection = db[os.getenv("COLLECTION_NAME", "people")]

@app.route("/")
def index():
    day = datetime.today().strftime("%A")
    time = datetime.now().strftime("%H:%M:%S")
    return render_template("index.html", day_of_week=day, current_time=time)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip()
    if not name or not role:
        return redirect(url_for("failure", reason="Name and role are required"))
    # auto increment id
    last = collection.find_one(sort=[("id", -1)])
    new_id = (last["id"] + 1) if last and isinstance(last.get("id"), int) else 1
    entry = {"id": new_id, "name": name, "role": role}
    try:
        collection.insert_one(entry)
    except Exception:
        return redirect(url_for("failure", reason="Database insert failed"))
    return redirect(url_for("success", name=name))

@app.route("/success")
def success():
    name = request.args.get("name", "User")
    return render_template("success.html", name=name)

@app.route("/failure")
def failure():
    reason = request.args.get("reason", "Unknown error")
    return render_template("failure.html", reason=reason)

@app.route('/todo')
def todo():
    return render_template('todo.html')

if __name__ == "__main__":
    app.run(debug=True)

from flask import request
from pymongo import MongoClient

# Replace with your actual MongoDB URI
client = MongoClient("mongodb://codeblink31:Welcome%40codeblink31@ac-h3tpu0p-shard-00-00.3ceun6a.mongodb.net:27017,ac-h3tpu0p-shard-00-01.3ceun6a.mongodb.net:27017,ac-h3tpu0p-shard-00-02.3ceun6a.mongodb.net:27017/?ssl=true&replicaSet=atlas-udfj2j-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
db = client["todo_db"]
collection = db["items"]

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    
    # Insert into MongoDB
    collection.insert_one({
        "name": item_name,
        "description": item_description
    })
    
    return "To-Do item submitted successfully!"
