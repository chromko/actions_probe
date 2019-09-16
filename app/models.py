from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    date = db.Column(db.String(16), unique = True)

    def __repr__(self):
        return '<User %r>' % (self.username)
