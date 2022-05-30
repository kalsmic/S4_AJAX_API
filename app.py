from flask import Flask
from model import db, migrate, config
from api.interests import interests_blueprint
from api.students import students_blueprint

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    app.config['SECRET_KEY'] = config['SECRET_KEY']
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()
app.register_blueprint(interests_blueprint)
app.register_blueprint(students_blueprint)

@app.route('/',methods=['POST'])
def index():
    return 'index.html'


