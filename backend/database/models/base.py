from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from database.manage_db import engine

Model = declarative_base()

session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
Model.query = session.query_property()
