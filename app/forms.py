from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User, ChoreList
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    type = SelectField('User Type', validators=[DataRequired()], choices=['Parent', 'Child', 'Friend'])
    approval_code = IntegerField('Approver Code', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # password2 = PasswordField(
    #     'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    point_balance = IntegerField('Point Balance', validators=[DataRequired()])
    cash_balance = IntegerField('Cash Balance', validators=[DataRequired()])
    user_type = SelectField('User Type', validators=[DataRequired()], choices=['Parent', 'Child', 'Friend'])
    is_active = SelectField('Is Active', validators=[DataRequired()], choices=['Yes', 'No'])
    approval_code = IntegerField('Approver Code', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


# Query Factory


def user_parent_query():
    return User.query.filter_by(user_type='Parent', is_active='Yes')


def user_child_query():
    return User.query.filter(User.user_type.isnot('Parent'), User.is_active.is_('Yes')).all()


def chore_query():
    return ChoreList.query.all()


class AddChoreForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    occurrence = SelectField('Frequency', validators=[DataRequired()], choices=['Daily', 'Weekly', 'Monthly'])
    created_by = QuerySelectField(query_factory=user_parent_query,  validators=[DataRequired()],
                                                                get_label='username')
    value = IntegerField('Chore Value', validators=[DataRequired(), NumberRange(0, 50, "Number between 0 and 50")])

    submit = SubmitField('Add Chore')


class EditChoreForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    occurrence = SelectField('Frequency', validators=[DataRequired()], choices=['Daily', 'Weekly', 'Monthly'])
    created_by = QuerySelectField(query_factory=user_parent_query,  validators=[DataRequired()],
                                  get_label='username')
    value = IntegerField('Chore Value', validators=[DataRequired(), NumberRange(0, 50, "Number between 0 and 50")])

    submit = SubmitField('Save Changes')


class AssignChoreForm(FlaskForm):
    assign_to = QuerySelectField(query_factory=user_child_query, validators=[DataRequired()],
                                 get_label='username')
    assign_chore = QuerySelectField(query_factory=chore_query, validators=[DataRequired()], get_label='description')

    chore_occurrence = StringField('Occurrence', render_kw={'readonly': True})
    chore_value = StringField('Value', render_kw={'readonly': True})
    assigned_by = QuerySelectField(query_factory=user_parent_query,  validators=[DataRequired()],
                                  get_label='username', default='Select')
    submit = SubmitField('Save')

class ChoreApproval(FlaskForm):
    approved_by = QuerySelectField(query_factory=user_parent_query, validators=[DataRequired()], get_label='username')
    approval_code = IntegerField('Approval Code', validators=[DataRequired()])
    submit = SubmitField('Approve')

