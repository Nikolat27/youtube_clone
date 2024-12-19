from sqlalchemy import create_engine


DB_USERNAME = "postgres"
DB_PASSWORD = "235691gg"
DB_HOST = "127.0.0.1"
DB_PORT = "5462"
DB_NAME = "youtube_db"

DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)

