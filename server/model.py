""" Models and database functions for project db """
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from server import app
db = SQLAlchemy(app)


class User(db.Model):
    """ User's details like username, password """

    __tablename__ = "Users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.Binary, nullable=True)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<User-{} user_id={}>".format(self.user_id, self.email)


class Problems(db.Model):
    """ Problems with id. """

    __tablename__ = "Problems"

    problem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    problem_level = db.Column(db.String(200), nullable=False)
    problem_title = db.Column(db.String(100), nullable=False)
    problem_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<Problem_id={} title={} Level={}>".format(
            self.problem_id, self.problem_title, self.problem_level
        )


class UserProblems(db.Model):
    """ Leetcode problems with properties specific to the user"""

    __tablename__ = "UserProblems"

    userproblem_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_level = db.Column(db.String(10), nullable = False)
    user_comments = db.Column(db.String(100), nullable = True)
    problem_id = db.Column(db.Integer, db.ForeignKey("Problems.problem_id"), nullable=False)

    def __repr__(self):
        """Provide useful output when printing."""

        return "<UserProblem_id={} Problem_id={} Level={}>".format(
            self.userproblem_id, self.problem_id, self.problem_level
        )



# -------------------------------------------------------------------
# Helper functions

URI = "postgresql://localhost/leetcodeproblems"
def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    app = Flask(__name__)
    
    connect_to_db(app, URI)

    print("Connected to DB.")


def connect_to_db(app, URI):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app

    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
