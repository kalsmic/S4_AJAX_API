from flask import Flask, request, Blueprint, abort, jsonify
from model import db, Student, Interest
from sqlalchemy.exc import SQLAlchemyError

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
    data = request.get_json()
    if len(data) > 0:
        name = data.get('name', None)
        interests = data.get('interests', None)
        if name is not None:
            student = Student(name=name)
            success = False
            try:
                student.add()
                for i in interests:
                    interest = Interest.query.filter(
                        Interest.id == i).one_or_none()
                    student.interests.append(interest)
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
        else:
            abort(400)
    else:
        abort(400)
