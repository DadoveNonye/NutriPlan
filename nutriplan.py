from app import create_app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, MealPlan , Meal, FoodItem, FoodIntake

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'MealPlan': MealPlan, 'Meal': Meal,
            'FoodItem': FoodItem, 'FoodIntake': FoodIntake, 'sa': sa, 'so': so}

