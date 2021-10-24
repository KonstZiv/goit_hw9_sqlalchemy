from os import environ
from dotenv import load_dotenv

load_dotenv()

conn_str = environ.get('CONNECTION_STRING') if environ.get(
    'CONNECTION_STRING') else None
