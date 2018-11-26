from homepg import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    household_id = db.Column(db.Integer, db.ForeignKey('household.id'), nullable = False, default = -1)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.household_id}')"


class Household(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable = False)
	users = db.relationship('User', backref='household', lazy = True)

