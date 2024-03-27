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
@login_required
def get_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    response = user.to_dict()
    response['uri'] = url_for('api.get_user', id=user.id)
    return response, 201


