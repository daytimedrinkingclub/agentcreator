# app/services/data_service.py
from extensions import db
import json
from sqlalchemy import desc
from models.models import Chat, Message

class DataService:
    @staticmethod
    # service to get chat by id
    def get_project_by_id(project_id):
        print(f"----------Getting project by ID: {project_id}----------")
        return Chat.query.get(project_id)

    @staticmethod
    # service to get all chats from the database
    def get_all_projects():
        print(f"----------Getting all projects from database----------")
        return Chat.query.all()

    @staticmethod
    # service to create a new chat
    def new_project():
        new_project = Chat()
        db.session.add(new_project)
        db.session.commit()
        print(f"----------New Project created with ID: {new_project.id}----------")
        return str(new_project.id)

    @staticmethod
    # service to save a message to the database
    def save_message(project_id, role, content, tool_use_id=None, tool_use_input=None, tool_name=None, tool_result=None):
        print(f"----------Saving message to database----------")
        message = Message(
            chat_id=project_id,
            role=role,
            content=content,
            tool_name=tool_name,
            tool_use_id=tool_use_id,
            tool_input=tool_use_input,
            tool_result=tool_result
        )
        db.session.add(message)
        db.session.commit()
        print(f"----------Message saved to database----------")
        return message
    
    @staticmethod
    # service to load the conversation from the database
    def load_conversation(project_id):
        print(f"----------Loading conversation from database----------")
        messages = Message.query.filter_by(chat_id=project_id).order_by(Message.created_at).all()
        conversation = []
        for message in messages:
            if message.role == "user":
                if message.tool_result:
                    conversation.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": message.tool_use_id,
                                "content": message.tool_result
                            }
                        ]
                    })
                else:
                    conversation.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message.content
                            }
                        ]
                    })
            elif message.role == "assistant":
                if message.tool_name:
                    conversation.append({
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": message.content
                            },
                            {
                                "type": "tool_use",
                                "id": message.tool_use_id,
                                "name": message.tool_name,
                                "input": message.tool_input
                            }
                        ]
                    })
                else:
                    conversation.append({
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": message.content
                            }
                        ]
                    })
        print(f"----------Conversation loaded from database----------")
        return conversation
    
    @staticmethod
    def get_project_summary(project_id):
        print(f"----------Getting project summary from database----------")
        # service to get the chat summary only
        chat = Chat.query.get(project_id)
        if not chat:
            return None
        last_message = Message.query.filter_by(chat_id=project_id).order_by(desc(Message.created_at)).first()
        message_count = Message.query.filter_by(chat_id=project_id).count()
        print(f"----------Project summary loaded from database----------")
        return {
            "id": chat.id,
            "last_message": last_message.content[:50] + "..." if last_message else None,
            "message_count": message_count,
            "created_at": chat.created_at
        }