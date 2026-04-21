from flask import Blueprint, flash, redirect, render_template, request, url_for

from control.create_user_profile_controller import create_user_profile_controller
from entity.user_profile import UserProfile

user_profile_bp = Blueprint("user_profile", __name__)

@user_profile_bp.route("/")
def home():
    return redirect(url_for('user_profile.list_profiles'))

@user_profile_bp.route("/profiles")
def list_profiles():
    profiles = UserProfile.getAllProfiles()
    return render_template("profiles/list_profiles.html", profiles=profiles)