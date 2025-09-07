import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "campus.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# =========================
# MODELS
# =========================
class College(db.Model):
    __tablename__ = "colleges"
    college_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.college_id"), nullable=False)


class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Workshop / Fest / Seminar
    date = db.Column(db.String(50), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.college_id"), nullable=False)
    is_cancelled = db.Column(db.Boolean, default=False)


class Registration(db.Model):
    __tablename__ = "registrations"
    reg_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)


class Attendance(db.Model):
    __tablename__ = "attendance"
    att_id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, db.ForeignKey("registrations.reg_id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Present / Absent


class Feedback(db.Model):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    feedback = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1–5


# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Campus Event Management API is running 🚀"})


# --- Create College ---
@app.route("/college", methods=["POST"])
def create_college():
    data = request.get_json(force=True)
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name'"}), 400
    college = College(name=data["name"])
    db.session.add(college)
    db.session.commit()
    return jsonify({"message": "College created", "college_id": college.college_id})


# --- Create Student ---
@app.route("/student", methods=["POST"])
def create_student():
    data = request.get_json(force=True)
    if not data or "name" not in data or "college_id" not in data:
        return jsonify({"error": "Missing 'name' or 'college_id'"}), 400
    student = Student(name=data["name"], college_id=data["college_id"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student created", "student_id": student.student_id})


# --- Create Event ---
@app.route("/event", methods=["POST"])
def create_event():
    data = request.get_json(force=True)
    required = ["title", "type", "date", "college_id"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing one of 'title','type','date','college_id'"}), 400
    event = Event(title=data["title"], type=data["type"], date=data["date"], college_id=data["college_id"])
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event created", "event_id": event.event_id})


# --- Register Student for Event ---
@app.route("/register", methods=["POST"])
def register_student():
    data = request.get_json(force=True)
    if not data or "student_id" not in data or "event_id" not in data:
        return jsonify({"error": "Missing 'student_id' or 'event_id'"}), 400

    # Prevent duplicate registration
    exists = Registration.query.filter_by(student_id=data["student_id"], event_id=data["event_id"]).first()
    if exists:
        return jsonify({"error": "Student already registered for this event"}), 400

    registration = Registration(student_id=data["student_id"], event_id=data["event_id"])
    db.session.add(registration)
    db.session.commit()
    return jsonify({"message": "Student registered", "reg_id": registration.reg_id})


# --- Mark Attendance ---
@app.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json(force=True)
    if not data or "reg_id" not in data or "status" not in data:
        return jsonify({"error": "Missing 'reg_id' or 'status'"}), 400
    attendance = Attendance(reg_id=data["reg_id"], status=data["status"])
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Attendance marked", "att_id": attendance.att_id})


# --- Submit Feedback ---
@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(force=True)
    required = ["event_id", "student_id", "feedback", "rating"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing one of 'event_id','student_id','feedback','rating'"}), 400
    if not (1 <= data["rating"] <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400
    feedback = Feedback(event_id=data["event_id"], student_id=data["student_id"],
                        feedback=data["feedback"], rating=data["rating"])
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback submitted", "feedback_id": feedback.feedback_id})


# --- Event Report (with average rating) ---
@app.route("/report/event/<int:event_id>", methods=["GET"])
def event_report(event_id):
    registrations = Registration.query.filter_by(event_id=event_id).all()
    attendees = Attendance.query.join(Registration, Attendance.reg_id == Registration.reg_id).filter(
        Registration.event_id == event_id, Attendance.status == "Present"
    ).count()
    feedbacks = Feedback.query.filter_by(event_id=event_id).all()
    avg_rating = round(sum(f.rating for f in feedbacks if f.rating) / len(feedbacks), 2) if feedbacks else None
    return jsonify({
        "event_id": event_id,
        "total_registrations": len(registrations),
        "attendees": attendees,
        "average_rating": avg_rating,
        "feedbacks": [f.feedback for f in feedbacks],
    })


# --- Attendance Percentage ---
@app.route("/report/event/<int:event_id>/attendance", methods=["GET"])
def event_attendance_percentage(event_id):
    total_regs = Registration.query.filter_by(event_id=event_id).count()
    attended = Attendance.query.join(Registration, Attendance.reg_id == Registration.reg_id).filter(
        Registration.event_id == event_id, Attendance.status == "Present"
    ).count()
    percentage = (attended / total_regs * 100) if total_regs > 0 else 0
    return jsonify({
        "event_id": event_id,
        "total_registered": total_regs,
        "attended": attended,
        "attendance_percentage": round(percentage, 2)
    })


# --- Popularity Report (with event type filter) ---
@app.route("/report/events/popularity", methods=["GET"])
def event_popularity():
    event_type = request.args.get("type")  # Optional filter
    query = (
        db.session.query(Event, db.func.count(Registration.reg_id).label("registrations"))
        .join(Registration, Registration.event_id == Event.event_id, isouter=True)
        .filter(Event.is_cancelled == False)
    )
    if event_type:
        query = query.filter(Event.type == event_type)
    events = query.group_by(Event.event_id).order_by(db.desc("registrations")).all()
    return jsonify([
        {"event_id": e.Event.event_id, "title": e.Event.title, "type": e.Event.type, "registrations": e.registrations}
        for e in events
    ])


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()      # Drops all tables
        db.create_all()    # Creates all tables
    app.run(debug=True)
