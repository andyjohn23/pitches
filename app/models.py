from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('pitch', backref='user', lazy='dynamic')
    comments = db.relationship('comments', backref='user', lazy='dynamic')
    like = db.relationship('likes',backref='user',lazy='dynamic')
    dislike = db.relationship('dislikes',backref='user',lazy='dynamic')
    pass_secure  = db.Column(db.String(255))

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User is {self.username}'
class pitch(db.Model):
    __tablename__ = 'pitch'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    post = db.Column(db.Text(), nullable = False)
    comment = db.relationship('comments',backref='pitch',lazy='dynamic')
    like = db.relationship('likes',backref='pitch',lazy='dynamic')
    dislike = db.relationship('dislikes',backref='pitch',lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)
    category = db.Column(db.String(255), index = True,nullable = False)
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

        
    def __repr__(self):
        return f'Pitch {self.post}'

class comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'),nullable = False)

    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comment = comments.query.filter_by(pitch_id=pitch_id).all()

        return comment

    
    def __repr__(self):
        return f'comment:{self.comment}'

class likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    
    def save_likes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_likes(cls,id):
        like = likes.query.filter_by(pitch_id=id).all()
        return like


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

class dislikes(db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    
    def save_dislikes(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_dislikes(cls,id):
        dislike = dislikes.query.filter_by(pitch_id=id).all()
        return dislike

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'

