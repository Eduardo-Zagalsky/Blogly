from flask_sqlalchemy import SQLAlchemy

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
        db.Text, default="https://cdn.vectorstock.com/i/preview-1x/66/14/default-avatar-photo-placeholder-profile-picture-vector-21806614.jpg")

    def __repr__(self):
        s = self
        return f"<User {s.id} {s.first_name} {s.last_name}>"


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column()
    user_code = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
