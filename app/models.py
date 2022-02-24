from app import db, ma
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
    is_active = db.Column(db.String(3), default='Yes')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<user {}>'.format(self.username)


class ChoreList(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    occurrence = db.Column(db.String(10))  # Daily, Weekly, Monthly, One_Off
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_chores = db.relationship('ChoreAssignments', backref='assignment_id')
    value = db.Column(db.Integer)

    def __repr__(self):
        return '<Chore {}>'.format(self.id)


class ChoreProgress(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer)
    status = db.Column(db.String(10))  # Complete, Incomplete, Pending, Expired
    assigned_user = db.Column(db.Integer)
    description = db.Column(db.String(128))
    due_date = db.Column(db.DateTime)  # based on the chore occurrence
    value = db.Column(db.Integer)
    occurrence = db.Column(db.String(10))

    def __repr__(self):
        return '<ChoreProgress {}>'.format(self.status)


class ChoreAssignments(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer, db.ForeignKey('chore_list.id'))

    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_by_id = db.Column(db.Integer)
    is_active = db.Column(db.String(3), default='Yes')

    def __repr__(self):
        return '<ChoreAssignment {}>'.format(self.id)


class ChoreListSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ChoreList
    id = ma.auto_field()
    description = ma.auto_field()
    occurrence = ma.auto_field()
    created_by_id = ma.auto_field()
    value = ma.auto_field()


class UserListSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    user_type = ma.auto_field()
    point_balance = ma.auto_field()
    cash_balance = ma.auto_field()
    is_active = ma.auto_field()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

