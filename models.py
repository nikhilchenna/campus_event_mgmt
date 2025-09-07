from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Colleges table
class College(db.Model):
    __tablename__ = "colleges"
    college_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Students table
class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.college_id"))


# Events table
class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Workshop/Fest/Seminar
    date = db.Column(db.String(50), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.college_id"))
    is_cancelled = db.Column(db.Boolean, default=False)  # Optional event cancellation


# Registrations table
class Registration(db.Model):
    __tablename__ = "registrations"
    reg_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))

    __table_args__ = (
        db.UniqueConstraint("student_id", "event_id", name="unique_registration"),
    )


# Attendance table

class Attendance(db.Model):
    __tablename__ = "attendance"
    att_id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.Integer, db.ForeignKey("registrations.reg_id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Present / Absent


# Feedback table
class Feedback(db.Model):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.String(250), nullable=True)
