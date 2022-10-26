from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def root():
    return redirect("/users")


@app.route("/users")
def users():
    # get users from database
    return render_template("users.html")


@app.route("/users/new")  # GET
def get_form():
    return render_template("new.html")


@app.route("/users/new")  # POST
def add_user():
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form["imgUrl"]
    # add to database
    return redirect("/users")


@app.route("/users/<int:user_id>")  # GET
def detail_page(user_id):
    return render_template("detail.html")


@app.route("/users/<int:user_id>/edit")  # GET
def get_user(user_id):
    return render_template("edit.html")


@app.route("/users/<int:user_id>/edit")  # POST
def edit_user(user_id):
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form["imgUrl"]
    return redirect("/users")


@app.route("/users/<int:user_id>/delete")  # POST
def delete_user():
    return redirect("/users")
