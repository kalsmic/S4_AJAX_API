from email import message
import sys
from flask import Flask, Blueprint, request, abort, jsonify, make_response
from model import db, Interest
from sqlalchemy.exc import SQLAlchemyError

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
    interest = Interest.query.filter(
        Interest.id == interest_id).one_or_none()
    if interest is not None:
        interest_f = [interest.format()]
        return jsonify({
            'success': True,
            'modified': interest_id,
            'interests': interest_f,
            'num_interests': 1
        })
    else:
        abort(500)


@interests_blueprint.route('/interests', methods=['POST'])
def create_interest():
    success = False
    data = request.get_json()
    if not len(data) or data.get('name', None)==None:
        abort(make_response(jsonify(message='Please provide an interest name '), 400))
    
    name = data.get('name', None)

    interest = Interest(name=name)
    success = False
    try:
        interest.add()
        interest.commit()
        interest.refresh()
        success = True
    except SQLAlchemyError:
        interest.rollback()
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
def update_interest(interest_id):
    success = False
    data = request.get_json()
    if not len(data) or data.get('name', None)==None:
        abort(make_response(jsonify(message='Please provide an interest name '), 400))

    name = data.get('name')

    try:
        interest.name = name
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
        Interest.id == interest_id).first_or_404()
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
