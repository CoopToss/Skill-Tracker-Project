from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True, nullable=False)
    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    goals = db.relationship('Goal', back_populates='user', lazy='dynamic')
    skills = db.relationship('Skill', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='goals')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    hours_logged = db.Column(db.Integer, default=0)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))  
    goal = db.relationship('Goal', backref='skills')  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_details = db.Column(db.Text, nullable=True)

class SkillLog(db.Model):
    __tablename__ = 'skill_logs'

    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
