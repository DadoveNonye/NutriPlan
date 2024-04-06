from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length, Regexp
from app.models import User
from app import db
import sqlalchemy as sa

class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), Regexp(
        r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])', message="Password must include at least one uppercase letter, one lowercase letter, and one digit.")
    ])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])

    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validate if the username is already taken.
        """
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        """
        Validate if the email address is already registered.
        """
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class ResetPasswordRequestForm(FlaskForm):
    """
    Form for requesting password reset.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    """
    Form for resetting password.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class CreateMealPlanForm(FlaskForm):
    mealName = StringField('Meal Name', validators=[DataRequired()])
    mealDescription = StringField('Meal Description')
