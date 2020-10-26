from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    '''
    Model class/db table for the user
    Args:
        db.Model: Connect our class to the database
    '''
    __tablename__  = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('pitch', backref='author', lazy='dynamic')
    pass_secure = db.Column(db.String())

    @property
    def password(self):
        '''
        Define property object to make limit access to pass_secure
        '''
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        '''
        Function to save a user
        '''
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.username}'

class pitch(db.Model):
    '''
    Model class to specify one to many relationship
    Args:
        db.Model: Connect our class to the database
    '''

    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    category = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('comment', backref='pitch', lazy='dynamic')

    def save_pitch(self):
        """
        Save Function
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'pitch {self.title}'


class comment(db.Model):
    '''
    Model table to store, access and manipulate comments
    '''
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))

    def save_comment(self):
        """
        Save Function
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
       return f'comment {self.content}'

