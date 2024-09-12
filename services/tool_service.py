import os
import re
import json
from .data_service import DataService
from .search_service import SearchService
from .anthropic_service import AnthropicService

# This class is called by the Toolhandler function
class Tools:
    @staticmethod
    def load_tools():
        tools_dir = os.path.join(os.path.dirname(__file__), "tools")
        tools = []
        for file_name in os.listdir(tools_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(tools_dir, file_name)
                with open(file_path, "r") as file:
                    tool_data = json.load(file)
                    tools.append(tool_data)
        print(f"----------Tools loaded and returned {len(tools)} tools----------")
        return tools
    
    @staticmethod
    def write_to_file(file_name, file_path, file_extension, content):
        # Ensure the file has a .txt extension
        if not file_name.endswith(file_extension):
            file_name += file_extension
        
        file_content = f"{content}"
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"----------Current directory: {current_dir}----------")
        # Create the full file path
        file_path = os.path.join(current_dir, file_path, file_name)
        print(f"----------File created at path: {file_path}----------")
        # Create and write to the text file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(file_content)
        
        return f"File '{file_name}' has been created in the current directory and the content has been written successfully."


    # this function is used to create a new project folder
    @staticmethod
    def create_project_folder(project_name):
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"----------Current directory: {current_dir}----------")
        # Create the full path for the new folder
        folder_path = os.path.join(current_dir, project_name)
        
        try:
            # Create the folder
            os.makedirs(folder_path, exist_ok=True)
            print(f"----------Folder created at path: {folder_path}----------")
            return f"Success: Folder '{project_name}' has been created."
        except OSError as e:
            print(f"----------Error creating folder: {e}----------")
            return f"Error: Failed to create folder '{project_name}'."
        
    # this function is used to create files within a project folder
    @staticmethod
    def create_file_in_project(project_name, file_name, file_path, file_extension, content):
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"----------Current directory: {current_dir}----------")
        # Create the full path for the new folder
        folder_path = os.path.join(current_dir, project_name)
        

# This class can be called to process the tool use and call the required tool and return the tool result
class ToolsHandler:
    @staticmethod
    def process_tool_use(tool_name, tool_input, tool_use_id, chat_id):
        print(f"----------process_tool_use functioned called----------")
        if tool_name == "code_writer":
            print(f"----------Calling code_writer tool----------")
            user_message = f"{tool_input['file_path'], tool_input['file_name'], tool_input['file_extension'], tool_input['code']}"
            result = AnthropicService.call_anthropic(tool_name, user_message)
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "search_tool":
            print(f"----------Calling search_tool tool----------")
            result = SearchService.search(tool_input["query"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "file_creator":
            print(f"----------Calling file_creator tool----------")
            user_message = f"{tool_input['project_name'], tool_input['file_name'], tool_input['file_path'], tool_input['file_extension']}"
            result = Tools.create_file_in_project(tool_input["project_name"], tool_input["file_name"], tool_input["file_path"], tool_input["file_extension"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "readme_writer":
            print(f"----------Calling readme_writer tool----------")
            result = Tools.write_to_file(tool_input["project_name"], tool_input["readme_file_content"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "project_creator":
            print(f"----------Calling project_creator tool----------")
            result = Tools.create_project_folder(tool_input["project_name"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        else:
            return "Error: Invalid tool name"