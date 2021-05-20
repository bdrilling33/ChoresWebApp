from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User
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
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


def user_type_query():
    return User.query.filter_by(user_type='Parent')


class AddChoreForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    occurrence = SelectField('Frequency', validators=[DataRequired()], choices=['Daily', 'Weekly', 'Monthly'])
    created_by = QuerySelectField(query_factory=user_type_query,  validators=[DataRequired()], get_label='username')
    value = IntegerField('Chore Value', validators=[DataRequired(), NumberRange(0, 50, "Number between 0 and 50")])

    submit = SubmitField('Add Chore')

