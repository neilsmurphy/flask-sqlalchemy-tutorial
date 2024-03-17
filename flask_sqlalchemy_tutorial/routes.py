"""Application routes."""
from datetime import datetime

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for

from .models import User, db


@app.route("/", methods=["GET"])
def user_records():
    """Create a user via query string parameters."""

    for key, value in request.args.items():
        print(f"Key: {key}, Value: {value}")
    username = request.args.get("user")
    email = request.args.get("email")
    bio = request.args.get('bio')
    print(username, email)
    if username and email:
        existing_user = User.query.filter(User.username == username or User.email == email).first()
        if existing_user:
            return make_response(f"{username} ({email}) already created!")
        new_user = User(
            username=username,
            email=email,
            created_at=datetime.now(),
            bio=bio,
            admin=False,
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for("user_records"))
    return render_template("users.jinja2", users=User.query.all(), title="All Users")
