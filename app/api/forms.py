from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, Length, Regexp
from app.models import User
from app import db
import sqlalchemy as sa


class CreateMealPlanForm(FlaskForm):
    """Form for mealplan creation """
    mealName = StringField('Meal Name', validators=[DataRequired()])
    mealDescription = StringField('Meal Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FoodIntakeForm(FlaskForm):
    food_item_id = IntegerField('Food Item ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Create Food Intake Entry')

