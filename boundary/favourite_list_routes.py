from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from control.add_favourite_list_controller import add_favourite_list_controller
from control.view_favourite_list_controller import view_favourite_list_controller
from control.search_favourite_list_controller import search_favourite_list_controller
from boundary.access_control import login_required, roles_required, DONOR


favourite_list_bp = Blueprint("favourites_list", __name__)


# =========================
# VIEW FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/view")
@login_required
@roles_required(DONOR)
def view_favourites_list():
    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()
    searchController = search_favourite_list_controller()
    viewController = view_favourite_list_controller()

    favourites = viewController.viewFavourites(account_id)

    if "search" in request.args:
        if search_term:
            favourites = searchController.searchFavourites(account_id, search_term)
        else:
            flash("Activity name or description required.", "error")

    if not favourites and search_term:
        flash("No matching favourite activities found.", "error")
        
    if not favourites:
        flash("No favourite activities found.", "error")

    return render_template(
        "favourites/view_favourites_list.html",
        favourites=favourites,
        search_term=search_term
    )


# =========================
# SEARCH FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/search")
@login_required
@roles_required(DONOR)
def search_favourites_list():
    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()

    controller = search_favourite_list_controller()
    favourites = []

    if "search" in request.args:
        if search_term:
            favourites = controller.searchFavourites(account_id, search_term)
        else:
            flash("Activity name or description required.", "error")

    if not favourites and search_term:
        flash("No matching favourite activities found.", "error")

    return render_template(
        "favourites/search_favourites_list.html",
        favourites=favourites,
        search_term=search_term
    )


# =========================
# ADD TO FAVOURITES
# =========================
@favourite_list_bp.route("/favourites/add", methods=["POST"])
@login_required
def add_favourite_list():
    if session.get("profile_id") != DONOR:
        return jsonify({
            "success": False,
            "message": "You do not have permission to access."
        }), 403

    account_id = session.get("account_id")
    activity_id = request.form.get("activityId")

    controller = add_favourite_list_controller()
    success, message = controller.addFavourite(account_id, activity_id)

    return jsonify({
        "success": success,
        "message": message
    })