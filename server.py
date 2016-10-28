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

    raw_emails = db.session.query(User.email).all()
    emails = [data[0] for data in raw_emails]
# Try getting one user instead of checking whole list
    if email not in emails:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.user_id
        print session
        flash('You are logged in!')

    return redirect("/")
# Should have separate route for loggin in existing users
@app.route("/logout")
def logout_user():
    """Log out the user"""
    session.clear() # Or take out value only
    flash('You are logged out')
    return redirect("/")

@app.route("/users/<user_id>") #Route syntax in python
def user_page(user_id):
    
    user = db.session.query(User).filter_by(user_id = user_id).one()

    # ratings = user.ratings
    # scores = []
    # scored_movies = []
    # for rating in ratings:
    #     scores.append(rating.score)
    #     scored_movies.append(rating.movie_id)
    # movie_objects = []
    # for movie in scored_movies:
    #     movie_objects.append(db.session.query(Movie).filter_by(movie_id = movie).one())
    # movies = []
    # for movie in movie_objects:
    #     movies.append(movie.title)

    return render_template("user.html", user=user)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    # app.run(port=5003)
    app.run(port=5000)
