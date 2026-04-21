from flask import Blueprint, flash, redirect, render_template, request, url_for

from control.create_user_profile_controller import create_user_profile_controller
from entity.user_profile import UserProfile

user_profile_bp = Blueprint("user_profile", __name__)

@user_profile_bp.route("/")
def home():
    return redirect(url_for('user_profile.list_profiles'))

@user_profile_bp.route("/profiles")
def list_profiles():
    search_term = request.args.get("search", "")

    if search_term.strip():
        profiles = UserProfile.searchProfiles(search_term)
    else:
        profiles = UserProfile.getAllProfiles()

    return render_template(
        "profiles/list_profiles.html",
        profiles = profiles,
        search_term = search_term
    )


@user_profile_bp.route("/profiles/create", methods=["GET", "POST"])
def create_profile():
    controller = create_user_profile_controller()

    if request.method == "POST":
        profile_name = request.form.get("profileName", "")
        profile_description = request.form.get("profileDescription", "")

        success, message, created_profile = controller.createUserProfile(
            profile_name,
            profile_description
        )
        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")

    return render_template("profiles/create_profile.html")