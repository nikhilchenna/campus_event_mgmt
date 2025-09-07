🎓 Campus Event Management System

A lightweight Flask + SQLite based web API to manage and track student participation in campus events such as workshops, fests, and seminars.
This project was built to satisfy assignment requirements and goes beyond with bonus features like reports, filtering, and attendance percentages.

🚀 Features

Event Management

Create and list events (with type filtering).

Cancel events (optional).

Student Management

Register students to colleges.

Prevent duplicate registrations for the same event.

Attendance & Feedback

Mark attendance for registered students.

Collect feedback with rating (1–5) and comments.

Reports

📊 Event Popularity (sorted by registrations).

📈 Student Participation (number of events attended).

⭐ Average Feedback Score per event.

🏆 Top 3 Most Active Students.

✅ Attendance Percentage per event (bonus).

🔎 Flexible filtering by event type.

🛠️ Tech Stack

Backend: Flask (Python)

Database: SQLite (via SQLAlchemy ORM)

Tools: Postman (API testing), PowerShell/Terminal

📂 Project Structure
campus_event_mgmt/                                                    
│                                                                                          
├── app.py # Main Flask application with API endpoints       
├── models.py # Database models (SQLAlchemy ORM)                                                       
├── campus.db # SQLite database (auto-created)                                                         
├── README.md # Project documentation                                                        
└── requirements.txt # Python dependencies

⚙️ Setup Instructions

Clone the repository:

git clone https://github.com/yourusername/campus_event_mgmt.git
cd campus_event_mgmt

Create and activate virtual environment:

python -m venv .venv
source .venv/bin/activate # Mac/Linux
.venv\Scripts\activate # Windows

Install dependencies:

pip install -r requirements.txt

Run the app:

python app.py

API will be live at:

http://127.0.0.1:5000

📌 Example API Usage
Create College
POST /college
Content-Type: application/json
{
"name": "REVA University"
}

Create Event
POST /event
Content-Type: application/json
{
"title": "AI Workshop",
"type": "Workshop",
"date": "2025-09-10",
"college_id": 1
}

Register Student for Event
POST /registration
Content-Type: application/json
{
"student_id": 1,
"event_id": 2
}

Event Popularity Report
GET /report/events/popularity

📊 Sample Reports

Event Popularity

[
{ "event": "Tech Fest", "registrations": 120, "avg_feedback": 4.5 },
{ "event": "AI Workshop", "registrations": 85, "avg_feedback": 4.2 }
]

Top 3 Most Active Students

[
{ "student": "Nikhil", "events_attended": 5 },
{ "student": "Asha", "events_attended": 4 },
{ "student": "Ravi", "events_attended": 3 }
]
