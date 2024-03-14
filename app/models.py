#!/usr/bin/python3
"""This module contains the models for NutriPlan application."""

from app import db

class MealPlan(db.Model):
    """ This class represents the meal plan model. """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    meals = db.relationship('Meal', backref='meal_plan', lazy='dynamic')

    def __repr__(self):
        return '<MealPlan {}>'.format(self.name)
    