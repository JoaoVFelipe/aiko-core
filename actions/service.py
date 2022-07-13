import requests
import os
from dotenv import load_dotenv

load_dotenv()

AIKO_API_URL = os.getenv('AIKO_API_URL')

def post_reminder(reminder_info):
