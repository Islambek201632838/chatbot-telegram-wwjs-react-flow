from app import db
from datetime import datetime

class ChatbotFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flow_data = db.Column(db.JSON)

class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    time = db.Column(db.Time, default=datetime.utcnow().time)
    whatsapp_user_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(50), unique=True)
    action = db.Column(db.String(50))  # Call or Write
