from homepg import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

association_table = db.Table('association', db.Model.metadata,
	db.Column('user', db.Integer, db.ForeignKey('user.id')),
	db.Column('household', db.Integer, db.ForeignKey('household.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    households = db.relationship("Household", secondary = association_table)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.household_id}')"


class Household(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable = False)