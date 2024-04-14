from flask import request, jsonify, render_template, flash, redirect, url_for
from app import db
from app.models import MealPlan, Meal
import sqlalchemy.orm as so
from app.api import bp
from flask_login import login_required, current_user
from app.models import FoodItem, FoodIntake
from flask_restful import reqparse
from datetime import date
from app.auth.forms import CreateMealPlanForm, FoodIntakeForm, FoodItemForm



@bp.route('/index', methods=['GET', 'POST'], strict_slashes=False)
@bp.route('/mealplans', methods=['GET', 'POST'])
@login_required
def create_meal_plan():

    form = CreateMealPlanForm()
    if form.validate_on_submit():
        name = form.mealName.data
        description = form.mealDescription.data

        meal_plan = MealPlan(user_id=current_user.id, name=name, description=description)
        db.session.add(meal_plan)
        db.session.commit()
        flash('Meal plan created successfully', 'success')
        return redirect(url_for('api.create_meal_plan'))

    return render_template('mealplans.html', title='Mealplan', form=form)


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


@bp.route('/food-item', methods=['GET'])
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
    form = FoodIntakeForm()

    if form.validate_on_submit():
        food_item_id = form.food_item_id.data
        quantity = form.quantity.data

        # Create a new FoodIntake object
        food_intake = FoodIntake(food_item_id=food_item_id, quantity=quantity)

        # Associate the new entry with the logged-in user
        food_intake.user_id = current_user.id

        # Save the new FoodIntake object to the database
        db.session.add(food_intake)
        db.session.commit()

        # Return a success message with the ID of the created entry
        return jsonify({'message': 'Food intake entry created', 'id': food_intake.id}), 201

    return jsonify({'error': 'Invalid form data'}), 400

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

@bp.route('/food-intake/today', methods=['GET'])
@login_required
def get_today_calories():
    user_id = current_user.id
    today = date.today()

    # Filter FoodIntake entries for the logged-in user and today's date
    food_intakes = FoodIntake.query.filter_by(user_id=user_id, date=today).all()

    total_calories = 0
    for intake in food_intakes:
        food_item = FoodItem.query.get(intake.food_item_id)
        total_calories += food_item.calories * intake.quantity

    return jsonify({'calories': total_calories})


@bp.route('/food-items', methods=['POST', 'GET'])
@login_required
def create_food_item():
    form = FoodItemForm()

    if form.validate_on_submit():
        name = form.name.data
        calories = form.calories.data
        protein = form.protein.data
        carbs = form.carbs.data
        fat = form.fat.data

        # Check if the correct data types are used
        if not isinstance(name, str):
            flash('Invalid data type for name', 'error')
        elif not isinstance(calories, int):
            flash('Invalid data type for calories', 'error')
        elif not isinstance(protein, int, float):
            flash('Invalid data type for protein', 'error')
        elif not isinstance(carbs, float, int):
            flash('Invalid data type for carbs', 'error')
        elif not isinstance(fat, float, int):
            flash('Invalid data type for fat', 'error')
        else:
            # Create a new FoodItem object
            food_item = FoodItem(name=name, calories=calories, protein=protein, carbs=carbs, fat=fat)

            # Associate the new entry with the logged-in user (if applicable)
            food_item.user_id = current_user.id

            # Save the new FoodItem object to the database
            db.session.add(food_item)
            db.session.commit()

            flash('Food item Data recorded successfully', 'success')
            return redirect(url_for('auth.index'))

    return render_template('fooditems.html', title='Food Item', form=form)
        