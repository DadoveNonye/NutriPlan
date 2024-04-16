#!/usr/bin/python3
"""This module contains the models for NutriPlan application."""

from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    """This class represents the user model.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        email (str): The email address of the user.
        meal_plans (WriteOnlyMapped['MealPlan']): The meal plans associated with the user.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(255), index=True,
                                        unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(255),
                                                nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(255),
                                             index=True, unique=True)
    meal_plans: so.WriteOnlyMapped['MealPlan'] = so.relationship(
         backref='user', lazy=True)
 
    def set_password(self, password):
        """Set the password for the user.

        Args:
            password (str): The password to be set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
@login_manager.user_loader
def load_user(id):
    """Load a user by their ID.

    Args:
        id (int): The ID of the user.

    Returns:
        User: The user object.
    """
    return db.session.get(User, int(id))
        
class MealPlan(db.Model):
    """This class represents the meal plan model.

    Attributes:
        id (int): The unique identifier for the meal plan.
        user_id (int): The ID of the user associated with the meal plan.
        name (str): The name of the meal plan.
        description (str): The description of the meal plan.
        meals (WriteOnlyMapped['Meal']): The meals associated with the meal plan.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                       index=True, nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    meals: so.WriteOnlyMapped['Meal'] = so.relationship(backref='meal_plan',
                                                        lazy=True)    

    def serialize(self):
        """Serialize the meal plan object.

        Returns:
            dict: The serialized meal plan object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def __repr__(self):
        return '<MealPlan {}>'.format(self.name)
   
class Meal(db.Model):
    """This class represents the meal model.

    Attributes:
        id (int): The unique identifier for the meal.
        meal_plan_id (int): The ID of the meal plan associated with the meal.
        name (str): The name of the meal.
        date (Optional[sa.Date]): The date of the meal.
        food_intakes (WriteOnlyMapped['FoodIntake']): The food intakes associated with the meal.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    meal_plan_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(MealPlan.id),
                                          index=True, nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    date: so.Mapped[Optional[sa.Date]] = so.mapped_column(sa.Date, nullable=False)
    food_intakes: so.WriteOnlyMapped['FoodIntake'] = so.relationship(
        backref='meal', lazy=True)

    def __repr__(self):
        return '<Meal {}>'.format(self.name)

class FoodItem(db.Model):
    """This class represents the food item model.

    Attributes:
        id (int): The unique identifier for the food item.
        name (str): The name of the food item.
        calories (int): The number of calories in the food item.
        protein (int): The amount of protein in the food item.
        carbs (int): The amount of carbs in the food item.
        fat (int): The amount of fat in the food item.
        food_intakes (WriteOnlyMapped['FoodIntake']): The food intakes associated with the food item.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    calories: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    protein: so.Mapped[int] = so.mapped_column(sa.Float, nullable=False)
    carbs: so.Mapped[int] = so.mapped_column(sa.Float, nullable=False)
    fat: so.Mapped[int] = so.mapped_column(sa.Float, nullable=False)
    food_intakes: so.WriteOnlyMapped['FoodIntake'] = so.relationship(
        backref='food_item', lazy=True)

    def __repr__(self):
        return '<FoodItem {}>'.format(self.name)

class FoodIntake(db.Model):
    """This class represents the food intake model.

    Attributes:
        id (int): The unique identifier for the food intake.
        user_id (int): The ID of the user associated with the food intake.
        food_item_id (int): The ID of the food item associated with the food intake.
        date (sa.Date): The date of the food intake.
        quantity (int): The quantity of the food intake.
        meal_id (Optional[int]): The ID of the meal associated with the food intake.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                       index=True, nullable=False)
    food_item_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(FoodItem.id),
                                          index=True, nullable=False)
    date: so.Mapped[sa.Date] = so.mapped_column(sa.Date, nullable=False)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    meal_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Meal.id),
                                                index=True)

    def __repr__(self):
        return '<FoodIntake {}>'.format(self.id)
