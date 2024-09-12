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
    - models.py # models file
    - routes.py # routes file
    - agent.py # the Anthropic ai agent
    - output/ # folder to store the output of the ai agent
        - projecta/ # the projects that will be created by the AI agent
        - projectb/ # sample project name and folder

```
