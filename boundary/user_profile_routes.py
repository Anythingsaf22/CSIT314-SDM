from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.search_user_profile_controller import search_user_profile_controller
from control.create_user_profile_controller import create_user_profile_controller
from control.view_user_profile_controller import view_user_profile_controller
from control.update_user_profile_controller import update_user_profile_controller
from control.delete_user_profile_controller import delete_user_profile_controller

user_profile_bp = Blueprint("user_profile", __name__)

@user_profile_bp.route("/")
def home():
    return redirect(url_for('user_profile.list_profiles'))

@user_profile_bp.route("/profiles")
def list_profiles():
    search_term = request.args.get("search", "")
    controller = search_user_profile_controller()

    if "search" in request.args:
        if search_term.strip():
            profiles = controller.searchProfiles(search_term)

        else:
            flash("Profile name or description needs to be provided.", "error")
            profiles = []
    else:
        profiles = 0
    return render_template(
        "profiles/list_profiles.html",
        profiles = profiles,
        search_term = search_term
    )


@user_profile_bp.route("/profiles/create", methods=["GET", "POST"])
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

@user_profile_bp.route("/profiles/view")
def view_profile():
    controller = view_user_profile_controller()
    profiles = controller.viewUserProfile()
    if not profiles:
        flash("No user profiles found.", "error")
        return render_template("profiles/view_profile.html")
    return render_template("profiles/view_profile.html", profiles=profiles)


@user_profile_bp.route("/profiles/update", methods=["GET", "POST"])
def update_profile():
    controller = update_user_profile_controller()

    if request.method == "POST":
        profile_id = request.form.get("profileId", "").strip()
        profile_name = request.form.get("profileName", "").strip()
        profile_description = request.form.get("profileDescription", "").strip()

        if not profile_id:
            flash("Profile ID is required.", "error")
            return render_template("profiles/update_profile.html")
        
        if not profile_name:
            flash("Profile name is required.", "error")
            return render_template("profiles/update_profile.html")
        
        if not profile_description:
            flash("Profile description is required.", "error")
            return render_template("profiles/update_profile.html")   
             
        success, message = controller.updateUserProfile(
            profile_id,
            profile_name,
            profile_description
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")

    return render_template("profiles/update_profile.html")

@user_profile_bp.route("/profiles/delete", methods=["GET", "POST"])
def delete_profile():
    controller = delete_user_profile_controller()

    if request.method == "POST":
        profile_id = request.form.get("profileId", "").strip()

        if not profile_id:
            flash("Profile ID is required.", "error")
            return render_template("profiles/delete_profile.html")
             
        success, message = controller.deleteUserProfile(
            profile_id,
        )

        if success:
            flash(message, "success")
            return redirect(url_for("user_profile.list_profiles"))

        flash(message, "error")

    return render_template("profiles/delete_profile.html")