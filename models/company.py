from sqlalchemy import Column,Integer,String,Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Company(Base):
    __tablename__="companies"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False,index=True)
    email = Column(String,unique=True)
    phone = Column(String,unique=True)

