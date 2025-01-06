from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class FoodItem(db.Model):
    __tablename__ = "food_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    cookingTime = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

