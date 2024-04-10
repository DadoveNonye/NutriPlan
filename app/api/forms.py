from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length, Regexp
from app.models import User
from app import db
import sqlalchemy as sa


class CreateMealPlanForm(FlaskForm):
    """Form for mealplan creation """
    mealName = StringField('Meal Name', validators=[DataRequired()])
    mealDescription = StringField('Meal Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


