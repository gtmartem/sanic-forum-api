USER = "postgres"
PASSWORD = "0a610292api"
IP = "127.0.0.1"
PORT = "5430"
DB = "forum"
URL = 'postgresql://{}:{}@{}:{}/{}'
DB_URL = URL.format(USER, PASSWORD, IP, PORT, DB)
