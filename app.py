from flask import Flask, render_template, request
from flask_migrate import Migrate

from api.interests import interests_blueprint
from api.students import students_blueprint
from model import db, Student, Interest


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


app = create_app()
app.register_blueprint(interests_blueprint)
app.register_blueprint(students_blueprint)


@app.route('/', methods=['GET'])
def index():
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    students = Student.query.order_by(
        Student.id.desc()).limit(limit).offset(offset).all()
    students_f = [student.format() for student in students]
    interests = Interest.query.order_by(
        Interest.id.desc()).limit(limit).offset(offset).all()
    interests_f = [interest.format() for interest in interests]
    return render_template(
        'lists.html',
        students=students_f,
        interests=interests_f)


if __name__ =="__main__":
    app.run(debug=True)