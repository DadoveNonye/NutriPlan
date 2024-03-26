from flask import Blueprint, request, jsonify
from app import db
from app.models import MealPlan
import sqlalchemy.orm as so
from app.api import bp
from flask_login import login_required, current_user
from app.models import MealPlan




@bp.route('/mealplans', methods=['POST', 'GET'])
@login_required
def create_meal_plan():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    meal_plan = MealPlan(name=name, description=description)
    db.session.add(meal_plan)
    db.session.commit()

    return jsonify({
        'message': 'Meal plan created successfully',
        'meal_plan_id': meal_plan.id
    }), 201

def get_meal_plans():
        
    # Get the logged-in user's ID from users.py
    user_id = current_user.id

    meal_plans = MealPlan.query.filter_by(user_id=user_id).all()

    # Return a list of serialized MealPlan objects
    meal_plans_data = [meal_plan.serialize() for meal_plan in meal_plans]

    return jsonify(meal_plans_data), 200
