from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')
    

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    
    def save_u(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.username}'

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    post = db.Column(db.Text(), nullable = False)
    location=db.Column(db.String(255))
    link=db.Column(db.String(255))
    comment = db.relationship('Comment',backref='reviews',lazy='dynamic')
    upvote = db.relationship('Upvote',backref='reviews',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='reviews',lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)
    category = db.Column(db.String(255), index = True,nullable = False)
    
    def save_p(self):
        db.session.add(self)
        db.session.commit()

        
    def __repr__(self):
        return f'Review {self.post}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    review_id = db.Column(db.Integer,db.ForeignKey('reviews.id'),nullable = False)

    def save_c(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,review_id):
        comments = Comment.query.filter_by(review_id=review_id).all()

        return comments

    
    def __repr__(self):
        return f'comment:{self.comment}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    review_id = db.Column(db.Integer,db.ForeignKey('reviews.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(review_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.review_id}'
        
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    reviews_id = db.Column(db.Integer,db.ForeignKey('reviews.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(review_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.review_id}'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)