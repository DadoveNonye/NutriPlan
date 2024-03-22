from app import app, db
from app.models import User, MealPlan , Meal, FoodItem, FoodIntake

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'MealPlan': MealPlan, 'Meal': Meal,
            'FoodItem': FoodItem, 'FoodIntake': FoodIntake}

