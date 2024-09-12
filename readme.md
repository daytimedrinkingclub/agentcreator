# Shipstation Agent backend

- This is the backend server built using flask
- Here we are creating api endpoints which take in a text prompt and return a folder which is the complete ai built project
- The AI is anthropic
- We have a simple model
- We will create services that will create a project folder and a readme file

## Folder Structure for the backend 

```bash
- shipstation/
    - myvenv/ # local virtual environment
    - .env # environment variables
    - main.py # main application file
    - config.py # configuration file
    - extensions.py # extension file
    - models/
    - routes/
    - services/
    - agent.py # the Anthropic ai agent
    - requirements.txt # dependencies
```
