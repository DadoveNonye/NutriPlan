from flask import request, url_for, abort
from app import db
from app.models import User
from app.api import bp
from flask_login import login_required, current_user


@bp.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user_id(id):
    return db.get_or_404(User, id).to_dict()



@bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate user input data
    if not username or not password:
        return {'error': 'Username and password are required'}, 400

    # Check for username or email conflicts
    if User.query.filter_by(username=username).first():
        return {'error': 'Username already exists'}, 409

    if email and User.query.filter_by(email=email).first():
        return {'error': 'Email already exists'}, 409

    # Create a new User object with secure password hashing
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    response = {'message': 'User registered successfully'}
    response['user'] = user.to_dict()
    response['user']['uri'] = url_for('api.get_user', id=user.id)

    return response, 201

@bp.route('/user/<username>', methods=['GET'])
@login_required
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return user.to_dict()
@bp.route('/users/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    user = db.get_or_404(User, id)
    data = request.get_json()
    user.from_dict(data)
    db.session.commit()
    return user.to_dict()

@bp.route('/users/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


