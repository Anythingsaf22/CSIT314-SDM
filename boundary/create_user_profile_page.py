from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.create_user_profile_controller import create_user_profile_controller

create_user_profile_bp = Blueprint("create_user_profile", __name__)
@create_user_profile_bp.route("/profiles/create", methods=["GET", "POST"])
def create_profile():
    controller = create_user_profile_controller()

    if request.method == "POST":
        profile_name = request.form.get("profileName", "").strip()
        profile_description = request.form.get("profileDescription", "").strip()
        if not profile_name:
            flash("Profile name is required.", "error")
            return render_template("profiles/create_profile.html")
        
        if not profile_description:
            flash("Profile description is required.", "error")
            return render_template("profiles/create_profile.html")
        
        success, message = controller.createUserProfile(
            profile_name,
            profile_description
        )
        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")

    return render_template("profiles/create_profile.html")
