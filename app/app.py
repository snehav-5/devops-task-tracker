import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


def create_app(database_url=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        tasks = Task.query.order_by(Task.id.desc()).all()
        return render_template("index.html", tasks=tasks)

    @app.route("/add", methods=["POST"])
    def add():
        title = request.form.get("title", "").strip()
        if title:
            db.session.add(Task(title=title))
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/toggle/<int:task_id>")
    def toggle(task_id):
        task = db.session.get(Task, task_id)
        if task:
            task.done = not task.done
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<int:task_id>")
    def delete(task_id):
        task = db.session.get(Task, task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return redirect(url_for("index"))

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    @app.route("/api/tasks")
    def api_tasks():
        return jsonify([t.to_dict() for t in Task.query.all()])

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
