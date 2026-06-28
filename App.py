from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)

# Registration Model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Welcome to Event Registration System"

# Add User
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    user = User(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User Added Successfully"})

# Add Event
@app.route("/events", methods=["POST"])
def add_event():
    data = request.get_json()

    event = Event(
        title=data["title"],
        venue=data["venue"],
        date=data["date"]
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event Added Successfully"})

# View Events
@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()

    output = []

    for e in events:
        output.append({
            "id": e.id,
            "title": e.title,
            "venue": e.venue,
            "date": e.date
        })

    return jsonify(output)

# Register User for Event
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    registration = Registration(
        user_id=data["user_id"],
        event_id=data["event_id"]
    )

    db.session.add(registration)
    db.session.commit()

    return jsonify({"message": "Registration Successful"})

if __name__ == "__main__":
    app.run(debug=True)
