from flask import Flask, Blueprint, request, abort, jsonify
from model import db, Interest

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


@interests_blueprint.route('/interests', methods=['POST'])
def create_interest():
    data = request.get_json()
    if len(data) > 0:
        name = data.get('name', None)
        if name is not None:
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
                        'interests': [interest.format()],
                        'num_interests': 1
                    })
                else:
                    abort(500)
        else:
            abort(400)
    else:
        abort(400)


@interests_blueprint.route('/interests/<int:interest_id>', methods=['PATCH'])
def update_interest(interest_id):
    if len(request.form) > 0:
        name = request.form.get('name', None)
        if name is not None:
            interest = Interest.query.filter(
                Interest.id == interest_id).one_or_none()
            success = False
            try:
                interest.name = name
                interest.commit()
                success = True
            except SQLAlchemyError:
                interest.rollback()
            finally:
                interest.close()
                if success:
                    return redirect(url_for('view_interests'))
                else:
                    abort(500)
        else:
            abort(500)
    else:
        abort(500)


@interests_blueprint.route('/interests/<int:interest_id>', methods=['DELETE'])
def delete_interest(interest_id):
    if len(request.form) > 0:
        interest = Interest.query.filter(
            Interest.id == interest_id).one_or_none()
        success = False
        try:
            interest.delete()
            interest.commit()
            success = True
        except SQLAlchemyError:
            interest.rollback()
        finally:
            interest.close()
        if success:
            return redirect(url_for('view_interests'))
        else:
            abort(500)
    else:
        abort(400)
