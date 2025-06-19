from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "name": t.name, "done": t.done}
        for t in tasks
    ])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = Task(name=data["name"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "name": new_task.name, "done": new_task.done}), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.done = data["done"]
    db.session.commit()
    return jsonify({"message": "Task updated"})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

@app.route("/api/tasks", methods=["DELETE"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    return jsonify({"message": "All tasks cleared"})

if __name__ == "__main__":
    app.run(debug=True)
