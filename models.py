from sqlalchemy import Column, Integer, String, Float
from database import Base

class Student(Base):

  __tablename__ = "students"

  id = Column(Integer, primary_key=True, autoincrement="auto")
  first_name = Column(String)
  last_name = Column(String)
  age = Column(Integer)
  email = Column(String)
  course = Column(String)
  CGPA = Column(Float)
  academic_year = Column(Integer)