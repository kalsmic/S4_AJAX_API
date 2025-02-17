from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FyyurSession():
    def add(self) -> None:
        db.session.add(self)

    def delete(self) -> None:
        db.session.delete(self)

    def flush(self) -> None:
        db.session.flush()

    def commit(self) -> None:
        db.session.commit()

    def refresh(self) -> None:
        db.session.refresh(self)

    def rollback(self) -> None:
        db.session.rollback()

    def close(self) -> None:
        db.session.close()


student_interests = db.Table(
    'student_interests', db.Model.metadata, db.Column(
        'student_id', db.Integer(), db.ForeignKey('students.id')), db.Column(
            'interest_id', db.Integer(), db.ForeignKey('interests.id')))


class Interest(db.Model, FyyurSession):
    __tablename__ = 'interests'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def format(self) -> dict:
        return {'id': self.id, 'name': self.name}

    def __repr__(self) -> str:
        return f'{self.id} - {self.name}'


class Student(db.Model, FyyurSession):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    interests = db.relationship("Interest",
                                secondary=student_interests,
                                backref="students")

    def format(self) -> dict:
        return {'id': self.id, 'name': self.name, 'interests': [interest.format() for interest in self.interests]}

    def __repr__(self) -> str:
        return f'{self.id} - {self.name}'
