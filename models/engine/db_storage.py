#!/usr/bin/python3
"""Defines the DBStorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from os import getenv

class DBStorage:
    """Manages database storage for HBNB"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')
            ), pool_pre_ping=True
        )

    def all(self, cls=None):
        """Query all objects of a class from the database"""
        obj_dict = {}
        if cls:
            query = self.__session.query(cls).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            query = []
            for cls in classes:
                query.extend(self.__session.query(cls).all())

        for obj in query:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add a new object to the database session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload database session"""
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the session"""
        self.__session.remove()

