from flask import Blueprint, request, jsonify
from app import db
from app.models import MealPlan, Meal
import sqlalchemy.orm as so
from app.api import bp
from flask_login import login_required, current_user
from app.models import FoodItem



@bp.route('/mealplans', methods=['POST'])
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


@bp.route('/mealplans/<int:id>', methods=['GET'])
@login_required
def get_meal_plan(id):
    meal_plan = MealPlan.query.get(id)

    if meal_plan is None:
        return jsonify({'error': 'Meal plan not found'}), 404

    # Get associated meals
    meals = Meal.query.filter_by(meal_plan_id=id).all()
    associated_meals = [meal.serialize() for meal in meals]

    # Serialize meal plan object
    meal_plan_data = meal_plan.serialize()
    meal_plan_data['associated_meals'] = associated_meals

    return jsonify(meal_plan_data), 200


@bp.route('/mealplans', methods=['GET'])
@login_required
def get_meal_plans():
    # Get the logged-in user's ID from users.py
    user_id = current_user.id

    meal_plans = MealPlan.query.filter_by(user_id=user_id).all()

    # Return a list of serialized MealPlan objects
    meal_plans_data = [meal_plan.serialize() for meal_plan in meal_plans]

    return jsonify(meal_plans_data), 200




    @bp.route('/mealplans/<int:id>', methods=['PUT'])
    @login_required
    def update_meal_plan(id):
        meal_plan = MealPlan.query.get(id)

        if meal_plan is None:
            return jsonify({'error': 'Meal plan not found'}), 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('description', required=False)
        args = parser.parse_args()

        meal_plan.name = args.get('name', meal_plan.name)  # Use existing name if not provided
        meal_plan.description = args.get('description', meal_plan.description)

        db.session.commit()

        return jsonify({'message': 'Meal plan updated successfully'}), 200




        @bp.route('/mealplans/<int:id>', methods=['DELETE'])
        @login_required
        def delete_meal_plan(id):
            meal_plan = MealPlan.query.get(id)

            if meal_plan is None:
                return jsonify({'error': 'Meal plan not found'}), 404

            # Check if there are associated meals
            meals = Meal.query.filter_by(meal_plan_id=id).all()
            if meals:
                return jsonify({'error': 'Cannot delete meal plan with associated meals'}), 400

            db.session.delete(meal_plan)
            db.session.commit()

            return jsonify({'message': 'Meal plan deleted successfully'}), 200


@bp.route('/food-items', methods=['GET'])
@login_required
def search_food_items():
    search_term = request.args.get('q')

    if not search_term:
        return jsonify({'error': 'Please provide a search term'}), 400

    # Perform search against the name field
    food_items = FoodItem.query.filter(FoodItem.name.ilike(f'%{search_term}%')).all()

    # Return a list of matching food items with details
    food_items_data = [{'id': food_item.id, 'name': food_item.name} for food_item in food_items]

    return jsonify(food_items_data), 200



@bp.route('/food-intake', methods=['POST'])
@login_required
def create_food_intake():
    # Get the data from the request body
    data = request.get_json()
    food_item_id = data.get('food_item_id')
    quantity = data.get('quantity')

    # Check if the required fields are provided
    if not food_item_id or not quantity:
        return jsonify({'error': 'Please provide food item ID and quantity'}), 400

    # Create a new FoodIntake object
    food_intake = FoodIntake(food_item_id=food_item_id, quantity=quantity)

    # Associate the new entry with the logged-in user
    food_intake.user_id = current_user.id

    # Save the new FoodIntake object to the database
    db.session.add(food_intake)
    db.session.commit()

    # Return a success message with the ID of the created entry
    return jsonify({'message': 'Food intake entry created', 'id': food_intake.id}), 201


@bp.route('/food-intake', methods=['GET'])
@login_required
def get_food_intake_entries():
    user_id = current_user.id

    food_intake_entries = FoodIntake.query.filter_by(user_id=user_id).all()

    food_intake_data = []
    for entry in food_intake_entries:
        food_item = FoodItem.query.get(entry.food_item_id)
        entry_data = {
            'date': entry.date,
            'food_item': {
                'id': food_item.id,
                'name': food_item.name
            },
            'quantity': entry.quantity
        }
        food_intake_data.append(entry_data)

    return jsonify(food_intake_data), 200
