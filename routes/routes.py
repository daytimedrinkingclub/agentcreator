from flask import Blueprint, jsonify, request
from services.data_service import DataService
from services.agent import AnthropicChat
import os

main = Blueprint('main', __name__)

@main.route("/new_project", methods=["POST", "GET"])
def new_project():
    if request.method == "POST":
        project_id = DataService.new_project()
        return jsonify({"project_id": project_id})
    else:
        return jsonify({"message": "Please use POST method to create a new project"})

# route to start the development of a project
@main.route("/start_development/<project_id>", methods=["POST"])
def start_development(project_id):
    AnthropicChat.handle_chat(project_id, user_message=request.json.get("user_message"))
    return jsonify({"message": "Development started"})

# route to get the root path
@main.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the API"})

# route to handle environment variables
@main.route("/env", methods=["GET"])
def get_env():
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    database_url = os.getenv('DATABASE_URL')
    return jsonify({
        "ANTHROPIC_API_KEY": anthropic_api_key[:10] + "..." if anthropic_api_key else None,
        "DATABASE_URL": database_url[:10] + "..." if database_url else None
    })