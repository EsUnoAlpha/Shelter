from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    age = db.Column(db.Integer)
    pet_type = db.Column(db.String(50), nullable=False)
