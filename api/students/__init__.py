from flask import request, Blueprint, abort, jsonify, make_response
from sqlalchemy.exc import SQLAlchemyError

from model import Student, Interest

students_blueprint = Blueprint('students_blueprint', __name__)


@students_blueprint.route('/students', methods=['GET'])
def view_students(limit=5, offset=0):
    students = Student.query.order_by(
        Student.id.desc()).limit(limit).offset(offset).all()
    students_f = [student.format() for student in students]
    return jsonify({
        'success': True,
        'students': students_f,
        'num_students': len(students_f)
    })


@students_blueprint.route('/students', methods=['POST'])
def create_student():
    success = False
    data = request.get_json()
    if not len(data) or data.get('name', None) == None or data.get('interests', None) == None:
        abort(make_response(jsonify(message='Please provide a name and interest property '), 400))
    student_name = data.get('name')

    # check if Student name already exists
    if Student.query.filter(Student.name.ilike(student_name)).first():
        return jsonify({
            'success': False,
            'message': f"Student with specified name {student_name} already exists"
        }), 409

    interest_id_list = data.get('interests')
    interest_objects = Interest.query.filter(Interest.id.in_(interest_id_list)).all()
    student = Student(name=student_name, interests=interest_objects)
    try:

        student.commit()
        student.refresh()
        success = True
    except SQLAlchemyError as e:
        print(str(e.__dict__['orig']))
        student.rollback()
    finally:
        student_f = [student.format()]
        student.close()
        if success:
            return jsonify({
                'success': True,
                'students': student_f,
                'num_students': 1
            })
        else:
            abort(500)
