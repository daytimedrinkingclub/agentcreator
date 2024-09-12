from extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Chat(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    messages = db.relationship('Message', back_populates='chat', lazy='dynamic', cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = db.Column(UUID(as_uuid=True), db.ForeignKey('chat.id'), nullable=False)
    role = db.Column(db.Enum('user', 'assistant', name='role_enum'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tool_name = db.Column(db.Text, nullable=True)
    tool_use_id = db.Column(db.Text, nullable=True)
    tool_input = db.Column(db.JSON, nullable=True)
    tool_result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    chat = db.relationship('Chat', back_populates='messages')