#!/usr/bin/python3
"""This module contains the models for NutriPlan application."""

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """ This class represents the user model. """
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
        """ sets user password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ checks user password """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
        
class MealPlan(db.Model):
    """ This class represents the meal plan model. """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                       index=True, nullable=False)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    meals: so.WriteOnlyMapped['Meal'] = so.relationship(backref='meal_plan',
                                                        lazy=True)    

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def __repr__(self):
        return '<MealPlan {}>'.format(self.name)
   
class Meal(db.Model):
    """ This class represents the meal model. """
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
    """ This class represents the food item model. """
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
    """ This class represents the food intake model. """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                       index=True, nullable=False)
    food_item_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(FoodItem.id),
                                          index=True, nullable=False)
    date: so.Mapped[sa.Date] = so.mapped_column(sa.Date, nullable=False)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    def __repr__(self):
        return '<FoodIntake {}>'.format(self.id)

