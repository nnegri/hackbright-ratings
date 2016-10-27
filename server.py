"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, 
    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Rating, Movie)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")
    # a = jsonify([1,3])
    # return a

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():
    """Users register here"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Checks to see that if user already exists"""
    email = request.form.get("email")
    password = request.form.get("password")

    # if User.query.filter(User.email == email) != None:
    raw_emails = db.session.query(User.email).all()
    emails = [data[0] for data in raw_emails]

    if email not in emails:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('You are logged in!')

    return redirect("/")

@app.route("/logout")
def logout_user():
    """Log out the user"""
    flash('You are logged out')
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    # app.run(port=5003)
    app.run(port=5000)
