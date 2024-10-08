# app/services/context_service.py
from extensions import db
from models.models import Chat, Message

class ContextService:
    @staticmethod
    def build_context(chat_id):
        print(f"Building context for chat ID: {chat_id}")

        messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_at).all()
        print(f"Total messages loaded: {len(messages)}")

        context = []
        for message in messages:
            if message.role == "user":
                if message.tool_result:
                    context.append({
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
                    context.append({
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
                    context.append({
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
                    context.append({
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text",
                                "text": message.content
                            }
                        ]
                    })
                
        print(f"Total messages built in context: {len(context)}")
        print(f"Context------------------------\n\n {context} \n\n------------------------------")

        return context