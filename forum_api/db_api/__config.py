import os

USER = "postgres"
PASSWORD = "0a610292api"
IP = os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "127.0.0.1"
PORT = os.environ.get("DB_PORT") if os.environ.get("DB_PORT") else "5430"
DB = "forum"
URL = 'postgresql://{}:{}@{}:{}/{}'
DB_URL = URL.format(USER, PASSWORD, IP, PORT, DB)
