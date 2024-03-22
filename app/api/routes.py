from flask import Blueprint, request, jsonify
from app import db
from app.models import MealPlan
import sqlalchemy.orm as so
from app.api import bp


@bp.route('/mealplans', methods=['POST'])
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
