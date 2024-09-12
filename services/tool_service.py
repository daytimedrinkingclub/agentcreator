import os
import re
import json
from .data_service import DataService
from .search_service import SearchService

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
    def write_to_file(file_path, content):
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"----------Current directory: {current_dir}----------")
        
        # Create the full file path
        full_file_path = os.path.join(current_dir, file_path)
        print(f"----------Writing to file: {full_file_path}----------")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        # Write the content to the file
        with open(full_file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        return f"Success: File '{file_path}' has been created and the content has been written successfully."


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
    def create_file_in_project(file_path, file_name, file_extension):
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"----------Current directory: {current_dir}----------")
        # Create the full path for the new file
        full_file_path = os.path.join(current_dir, f"{file_path}")
        print(f"----------Creating file at path: {full_file_path}----------")
        
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            # Create the file
            with open(full_file_path, 'w') as f:
                pass  # Create an empty file
            return f"Success: File '{file_path}' has been created at {full_file_path}."
        except OSError as e:
            print(f"----------Error creating file: {e}----------")
            return f"Error: Failed to create file '{file_path}' at {full_file_path}."

# This class can be called to process the tool use and call the required tool and return the tool result
class ToolsHandler:
    @staticmethod
    def process_tool_use(tool_name, tool_input, tool_use_id, chat_id):
        print(f"----------process_tool_use functioned called----------")
        if tool_name == "code_writer":
            print(f"----------Calling code_writer tool----------")
            result = Tools.write_to_file(tool_input['file_path'], tool_input['code'])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "file_creator":
            print(f"----------Calling file_creator tool----------")
            result = Tools.create_file_in_project(tool_input["file_path"], tool_input["file_name"], tool_input["file_extension"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        
        elif tool_name == "project_creator":
            print(f"----------Calling project_creator tool----------")
            result = Tools.create_project_folder(tool_input["project_name"])
            DataService.save_message(chat_id, "user", content=result, tool_use_id=tool_use_id, tool_result=result)
            return result
        else:
            return "Error: Invalid tool name"