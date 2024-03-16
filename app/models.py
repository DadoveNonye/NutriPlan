#!/usr/bin/python3
"""This module contains the models for NutriPlan application."""

from app import db
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """ This class represents the user model. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)

    def set_password(self, password):
        """ sets user password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ checks user password """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class MealPlan(db.Model):
    """ This class represents the meal plan model. """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    meals = db.relationship('Meal', backref='meal_plan', lazy='dynamic')

    def __repr__(self):
        return '<MealPlan {}>'.format(self.name)
    