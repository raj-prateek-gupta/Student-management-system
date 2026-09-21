from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread":False})

class Base(DeclarativeBase):
  pass

SessionLocal = sessionmaker(
  autoflush=False,
  autocommit=False,
  bind=engine
)

