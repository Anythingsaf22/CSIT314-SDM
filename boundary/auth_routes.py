from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from control.login_controller import login_controller
from control.logout_controller import logout_controller

"""
Flow is: /login GET -> show form
/login POST -> authenticate + create session + store Flask session
/logout -> update DB session + clear Flask session
"""

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])

def login():
    controller = login_controller()
    if request.method == "POST":
        user_name = request.form.get("userName", "").strip()
        password = request.form.get("passWord", "").strip()
        success, message, account, user_session = controller.loginUser(user_name, password)

        if success:
            session["account_id"] = account.accountId
            session["profile_id"] = account.profileId
            session["user_name"] = account.userName
            session["session_id"] = user_session.sessionId

            flash(message, "success")
            return redirect(url_for("home"))

        flash(message, "error")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    controller = logout_controller()
    session_id = session.get("session_id")

    if session_id:
        success, message = controller.logoutUser(session_id)
        flash(message, "success" if success else "error")

    session.clear()
    return redirect(url_for("auth.login"))
