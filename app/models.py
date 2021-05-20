from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))  # Parent, Child, Friend
    point_balance = db.Column(db.Integer, default=0)
    cash_balance = db.Column(db.Integer, default=0)
    assigned_chores = db.relationship('ChoreAssignments', backref='assigned_to')
    created_chores = db.relationship('ChoreList', backref='created_by')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user {}>'.format(self.username)


class ChoreList(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    occurrence = db.Column(db.String(10))  # Daily, Weekly, Monthly, One_Off
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<Chore {}>'.format(self.description)


class ChoreProgress(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer)
    status = db.Column(db.String(10))  # Complete, Incomplete, Pending, Expired
    assigned_user_id = db.Column(db.Integer)
    due_date = db.Column(db.DateTime)  # based on the chore occurrence

    def __repr__(self):
        return '<ChoreProgress {}>'.format(self.status)


class ChoreAssignments(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<ChoreAssignment {}>'.format(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

