
""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Food(db.Model):
    __tablename__ = 'food'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _category = db.Column(db.String(255), unique=False, nullable=False)
    _time = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    #posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    """
    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, password="123qwerty", dob=date.today()):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.set_password(password)
        self._dob = dob
    """
        
    def __init__(self, name, category, time):
        self._name = name
        self._category = category 
        self._time = time 

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    @property 
    def category(self):
        return self._category
      
    @category.setter 
    def category(self, category):
        self._category = category 
    
    @property
    def time(self):
        return self._time
    
    @time.setter 
    def time(self, time):
        self._time = time 
        
    """
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
    """
    
    """
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        #Create a hashed password.
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        #Check against hashed password.#
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property
    def age(self):
        today = date.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    """ 
    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "time": self.time,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", category="", time=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(category) > 0:
            self.category = category
        if len(time) > 0:
            self.time(time)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initFood():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    """
    u1 = User(name='Thomas Edison', uid='toby', password='123toby', dob=date(1847, 2, 11))
    u2 = User(name='Nicholas Tesla', uid='niko', password='123niko')
    u3 = User(name='Alexander Graham Bell', uid='lex', password='123lex')
    u4 = User(name='Eli Whitney', uid='whit', password='123whit')
    u5 = User(name='John Mortensen', uid='jm1021', dob=date(1959, 10, 21))
    """
    dumplings = Food(name="dumplings", category="staple", time="120")
    steamedFish = Food(name="steamed fish", category="meat", time=120)

    foods = [dumplings]
    
    for food in foods:
        food.create()
"""
    #Builds sample user/note(s) data
    for food in foods:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")
""" 