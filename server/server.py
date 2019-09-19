"""LeetCode tracker"""

from jinja2 import StrictUndefined
import os
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    session,
    jsonify,
    json,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS, cross_origin
import requests
import bcrypt
from six import u


app = Flask(__name__, template_folder="../public", static_folder="../src") 
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/leetcodeproblems'
CORS(app)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# An undefined variable in Jinja2 will not fail silently:
app.jinja_env.undefined = StrictUndefined

from model import User, Problems, UserProblems, connect_to_db, db

@app.route("/register", methods=["POST"])
def register_form():
    """Registration form that takes email address, password and trigger words."""

    # Reg form is rendered when you go to page. When it is submitted, a
    # post request is made and if user's email is not in database then
    # it gets added and redirected to the homepage.

    data = request.data
    email = json.loads(data)["email"]
    # print("Email provided: ", email)
    password = json.loads(data)["password"]
    # print("Password provided: ", password)

    # Checking to see if the email provided is in the database
    # already.
    email_in_db = User.query.filter_by(email=email).first()

    if email_in_db is None:
        # print(email_in_db)
        new_user = User(email=email, password=hash_password(password), trig=triggers)
        db.session.add(new_user)
        db.session.commit()
        # print(f"New user created {email}")
        return jsonify("successfully added")
    else:
        # print(f"User already registered {email}")
        return jsonify("user already registered.")


@app.route("/logged-in", methods=["POST"])
def logged_in():
    """Logged in or not"""

    # This is how react (front-end) sends info to this route.
    data = request.data
    info = json.loads(data)
    email = info["email"]
    print("Email provided: ", email)
    password = info["password"]
    print("Password provided: ", password)

    # Checking to see if this email exists in the database.
    # Making a user object.
    email_in_db = User.query.filter(User.email == email).first()

    # Checking to see if the password matches for the email provided by the
    # user.
    if email_in_db:
        if bcrypt.checkpw(password.encode("utf8"), email_in_db.password):
            # If the check works for the email and matching password,
            # news options page is rendered. Otherwise, the login
            # page is rendered again.
            session["user"] = email

            # print("User id: ", user_id)
            # print("You have successfully logged in!")
            return jsonify("success")
        else:
            # print("Password incorrect.")
            return jsonify("Incorrect password")
    else:
        print("Couldn't find the given email. ")
        return jsonify("Please register.")


@app.route("/logout")
def logout():
    """Logged out and session cleared."""
    data = request.data
    session.clear()
    return jsonify("logged out")



# ------------------------------------------------------------------------------------------
# HELPER FUNCTIONS:
# ------------------------------------------------------------------------------------------


def hash_password(password):
    """ Given a string, hashes it using bcrypt"""
    # For password hashing
    u_password = u(password)
    encoded_password = u_password.encode("utf8")
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hashed_password


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, uri="postgresql://localhost/leetcodeproblems")

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000)
