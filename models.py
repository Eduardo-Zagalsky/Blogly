from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(10), nullable=False)
    last_name = db.Column(db.String(10), nullable=False)
    image_url = db.Column(
        db.Text, default="https://media.cheggcdn.com/media/d53/d535ce9a-4535-4e56-bd8e-81300a25a4f7/php4KwLCz")
    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def time_date(self):
        return self.created_at.strftime("%m/%d/%Y, %I:%M %p")
