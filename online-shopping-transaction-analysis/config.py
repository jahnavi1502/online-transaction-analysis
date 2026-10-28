import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "local-development-key")
    DB_CONFIG = dict(host=os.getenv("DB_HOST","127.0.0.1"), port=int(os.getenv("DB_PORT","3306")),
        user=os.getenv("DB_USER","root"), password=os.getenv("DB_PASSWORD",""),
        database=os.getenv("DB_NAME","shopping_analysis"))
