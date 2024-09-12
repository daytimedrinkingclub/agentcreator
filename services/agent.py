import os
import json
import anthropic
from datetime import datetime
from .data_service import DataService
from .context_service import ContextService
from .tool_service import Tools, ToolsHandler
from typing import List, Dict, Any

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
today = datetime.now().strftime("%Y-%m-%d")
class AnthropicChat:
    @staticmethod
    def process_conversation(chat_id: str) -> List[Dict[str, Any]]:
        tools = Tools.load_tools()
        conversation = ContextService.build_context(chat_id)
        print(f"process_conversation started with {chat_id} with current context_len: {len(conversation)}")
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            temperature=0,
            system=
            """
            Today is {today}.\n
            You are tasked to help the user with their day to day coding requirements.
            """,
            tools=tools,
            # tool_choice={"type": "auto"},
            messages=conversation,
        )
        print(f"Response Received from ANTHROPIC API: {response}")

        if response.stop_reason != "tool_use":
            # No tool use, return the final response
            print(f"No tool use, returning assistant response which needs a user message")
            DataService.save_message(chat_id, "assistant", content=response.content[0].text)
            return response

        # Handle tool use
        print(f"Tool use detected, processing tool use")
        tool_use = next(block for block in response.content if block.type == "tool_use")

        print(f"Tool Name: {tool_use.name}")
        
        DataService.save_message(chat_id, "assistant", content=response.content[0].text, tool_use_id=tool_use.id, tool_use_input=tool_use.input, tool_name=tool_use.name)

        tool_result = ToolsHandler.process_tool_use(tool_use.name, tool_use.input, tool_use.id, chat_id)

        print(f"Tool Result received: {tool_result}")

        if tool_result:
            # If a tool result is received, build the latest context and call process_conversation again
            conversation = ContextService.build_context(chat_id)
            return AnthropicChat.process_conversation(chat_id)

        return response

    @staticmethod
    def handle_chat(chat_id: str, user_message: str) -> str:
        prompt = """
        Today is {today}.\n
        Your task is to create small flask apps, the user will provide with the details of the flask app to be created \n
        You need to use the available tools to create the flask app, first create the project folder \n
        Then create a readme file with the basic details of the project \n
        Then create create all the required files with comments in the file which will help later AI code writing agents to write the code within them \n
        Then call the code writing agents with the file names and descriptions of the code to be created so that the files can be created
        """
        DataService.save_message(chat_id, "user", content=f'{prompt} {user_message}')
        # Process the conversation
        response = AnthropicChat.process_conversation(chat_id)
        # Extract the text content from the response
        return response