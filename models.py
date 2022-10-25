from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"


def __repr__(self):
    s = self
    if s.img:
        has_img = True
    else:
        has_img = False
    return f"<id = {s.id} name = {s.firstName} {s.lastName} img = {has_img}>"
