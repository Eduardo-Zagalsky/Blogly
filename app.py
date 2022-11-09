from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# USER _________________________________________________________________________________________________________________________________


@app.route("/")
def root():
    return redirect("/users")


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def get_form():
    return render_template("new.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form["imgUrl"]

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def detail_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["firstName"]
    user.last_name = request.form["lastName"]
    user.image_url = request.form["imgUrl"]
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

# POSTS ________________________________________________________________________________________________________________


@app.route("/users/<int:user_id>/posts/new")
def get_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post-form.html", user=user, tags=tags)


# Be more efficient
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    tag_ids = []
    user = User.query.get_or_404(user_id)
    tag_list = request.form.getlist("tags")
    for id in tag_list:
        tag_ids.append(int(id))
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(
        title=request.form["title"], content=request.form["content"], user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user.id}")


@app.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("post.html", posts=posts)


@app.route("/posts/<int:post_id>")
def post_info(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post-info.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def get_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post-edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    tag_ids = []
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_list = request.form.getlist("tags")
    for id in tag_list:
        tag_ids.append(int(id))
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.commit()
    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

# TAGS ___________________________________________________________________________________________________________


@app.route("/tags")
def tags():
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def tag_info(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-info.html", tag=tag)


@app.route("/tags/new")
def tag_form():
    return render_template("tag-form.html")


@app.route("/tags/new", methods=["POST"])
def new_tag():
    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-edit.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edited_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
