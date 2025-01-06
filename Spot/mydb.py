from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    cookingTime = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
