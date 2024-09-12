import os
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get('TAVILY_API_KEY'))
print(os.environ.get('ANTHROPIC_API_KEY'))
print(os.environ.get('DATABASE_URL'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://root@localhost/shipstation'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

