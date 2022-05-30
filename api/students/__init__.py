from flask import Flask, Blueprint, abort, jsonify
from model import db, Student

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
    if len(request.form) > 0:
        name = request.form.get('name', None)
        interests = request.form.getlist('interests', None)
        # print(interests)
        if name is not None:
            student = Student(name=name)
            success = False
            try:
                student.add()
                for i in interests:
                    print(i)
                    interest = Interest.query.filter(
                        Interest.id == i).one_or_none()
                    student.interests.append(interest)
                student.commit()
                student.refresh()
                success = True
            except SQLAlchemyError:
                student.rollback()
            finally:
                student.close()
            if success:
                return jsonify({
                    'success':True,
                    'students':[student.format()]
                    'num_students':1
                })
            else:
                abort(500)
        else:
            abort(400)
    else:
        abort(400)