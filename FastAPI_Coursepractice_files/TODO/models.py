## The models.py file is used to create a template(model) to 
# how the tables and columns inside a database how it should look like

from sqlalchemy import Boolean,Column,String,Integer, ForeignKey
from sqlalchemy.orm import relationship
from DataBase import base

# In here we imported a datatypes for a newly creating table columns and
#  imported a DataBase file that we prviously Created from the DataBase file we imported a Base into a todos Class 
class Users(base):
    __tablename__="users"
    id=Column(Integer, primary_key =True, index=True)
    email = Column(String, unique=True,index=True)
    username = Column(String, unique=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)
    todos = relationship("todos", back_populates="owner")


class todos(base):
    __tablename__="todos"

    """In todos class we specified all the columns that we need to store into the database
     and the data type of the columns"""
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean , default=False)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    owner = relationship("Users", back_populates = "todos")


