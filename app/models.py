from main import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    date = db.Column(db.String(16), unique = True)

    def __repr__(self):
        return '<User %r>' % (self.username)
