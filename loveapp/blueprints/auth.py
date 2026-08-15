from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

try:
    from ..extensions import db
    from ..forms import LoginForm
    from ..models import User
except ImportError:
    from extensions import db
    from forms import LoginForm
    from models import User

auth = Blueprint("auth", __name__, template_folder="../templates/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)

        user.login_count = (user.login_count or 0) + 1
        user.last_login_utc = datetime.now(timezone.utc)
        db.session.commit()

        next_page = request.args.get("next")
        # Guard against open redirects: only allow relative paths.
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("home")
        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))
