from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.add_favourite_list_controller import add_favourite_list_controller
from control.view_favourite_list_controller import view_favourite_list_controller
from control.search_favourite_list_controller import search_favourite_list_controller
from boundary.access_control import login_required, roles_required, DONOR

favourite_list_bp = Blueprint("favourite_list", __name__)

# VIEW + SEARCH
@favourite_list_bp.route("/favourites_list")
@login_required
@roles_required(DONOR)
def list_favourites():
    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()

    viewController = view_favourite_list_controller()
    searchController = search_favourite_list_controller()

    favourites = viewController.viewFavourites(account_id)

    if "search" in request.args:
        if search_term:
            favourites = searchController.searchFavourites(account_id, search_term)
        else:
            flash("Activity name or description required.", "error")

    if not favourites:
        flash("No favourite activities found.", "error")

    return render_template(
        "favourites/list_favourites.html",
        favourites=favourites,
        search_term=search_term
    )


# ADD
@favourite_list_bp.route("/favourites/add", methods=["POST"])
@login_required
@roles_required(DONOR)
def add_favourite_list():
    account_id = session.get("account_id")
    activity_id = request.form.get("activityId", "").strip()

    if not activity_id:
        flash("Activity ID is required.", "error")
        return redirect(url_for("fundraising_activity.list_activities"))

    controller = add_favourite_list_controller()
    success, message = controller.addFavourite(account_id, int(activity_id))

    flash(message, "success" if success else "error")

    return redirect(url_for("fundraising_activity.list_activities"))
