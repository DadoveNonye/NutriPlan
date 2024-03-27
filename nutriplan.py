from app import create_app, db
from app.models import User, MealPlan , Meal, FoodItem, FoodIntake

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'MealPlan': MealPlan, 'Meal': Meal,
            'FoodItem': FoodItem, 'FoodIntake': FoodIntake}

