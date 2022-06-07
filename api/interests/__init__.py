import sys

from flask import Blueprint, request, abort, jsonify
from sqlalchemy.exc import SQLAlchemyError

from helpers import validate_request
from model import Interest

interests_blueprint = Blueprint('interests_blueprint', __name__)


@interests_blueprint.route('/interests', methods=['GET'])
def view_interests(limit=5, offset=0):
    interests = Interest.query.order_by(
        Interest.id.desc()).limit(limit).offset(offset).all()
    interests_f = [interest.format() for interest in interests]
    return jsonify({
        'success': True,
        'interests': interests_f,
        'num_interests': len(interests_f)
    })


@interests_blueprint.route('/interests/<int:interest_id>', methods=['GET'])
def get_interest(interest_id):
    interest = Interest.query.get_or_404(interest_id)
    interest_f = [interest.format()]
    return jsonify({
        'success': True,
        'modified': interest_id,
        'interests': interest_f,
        'num_interests': 1
    })


@interests_blueprint.route('/interests', methods=['POST'])
@validate_request
def create_interest():
    success = False
    interest_name = name = request.get_json().get('name')
    # check if interest name already exists
    if Interest.query.filter(Interest.name.ilike(interest_name)).first():
        return jsonify({
            'success': False,
            'message': f"Interest with specified name {interest_name} already exists"
        }), 409

    interest = Interest(name=interest_name)

    try:
        interest.add()
        interest.commit()
        interest.refresh()
        success = True
    except SQLAlchemyError:
        interest.rollback()
        print(sys.exc_info())
    finally:
        interest.close()
        if success:
            return jsonify({
                'success': True,
                'created': interest.id,
                'interests': [interest.format()],
                'num_interests': 1
            })
        else:
            abort(500)


@interests_blueprint.route('/interests/<int:interest_id>', methods=['PATCH'])
@validate_request
def update_interest(interest_id):
    success = False
    interest = Interest.query.get_or_404(interest_id)
    try:
        interest.name = request.get_json().get('name')
        interest.commit()
        success = True
    except SQLAlchemyError:
        print(sys.exc_info())
        interest.rollback()
        print(sys.exc_info())
    finally:
        interest_f = [interest.format()]
        interest.close()
        if success:
            return jsonify({
                'success': True,
                'modified': interest_id,
                'interests': interest_f,
                'num_interests': 1
            })
        else:
            abort(500)


@interests_blueprint.route('/interests/<int:interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    interest = Interest.query.filter(
        Interest.id == interest_id).get_or_404()
    success = False
    try:
        interest.delete()
        interest.commit()
        success = True
    except SQLAlchemyError:
        print(sys.exc_info())
        interest.rollback()
    finally:
        interest.close()
    if success:
        return jsonify({
            'success': True,
            'deleted': interest_id
        })
    else:
        abort(500)
