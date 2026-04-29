from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.search_fundraising_activity_controller import search_fundraising_activity_controller
from control.create_fundraising_activity_controller import create_fundraising_activity_controller
from control.view_fundraising_activity_controller import view_fundraising_activity_controller
from control.update_fundraising_activity_controller import update_fundraising_activity_controller
from control.delete_fundraising_activity_controller import delete_fundraising_activity_controller

fundraising_activity_bp = Blueprint("fundraising_activity", __name__)


@fundraising_activity_bp.route("/")
def home():
    return redirect(url_for('fundraising_activity.list_activities'))

# LIST + SEARCH
@fundraising_activity_bp.route("/activities")
def list_activities():
    search_term = request.args.get("search", "")
    controller = search_fundraising_activity_controller()

    if "search" in request.args:
        if search_term.strip():
            activities = controller.searchActivities(search_term)
        else:
            flash("Activity name or description required.", "error")
            activities = []
    else:
        activities = 0

    return render_template(
        "activities/list_activities.html",
        activities=activities,
        search_term=search_term
    )

# CREATE
@fundraising_activity_bp.route("/activities/create", methods=["GET", "POST"])
def create_activity():
    controller = create_fundraising_activity_controller()

    if request.method == "POST":
        account_id = request.form.get("accountId", "").strip()
        category_id = request.form.get("categoryId", "").strip()
        name = request.form.get("name", "").strip()
        desc = request.form.get("desc", "").strip()
        goal = request.form.get("goal", "").strip()
        start_date = request.form.get("startDate", "").strip()
        end_date = request.form.get("endDate", "").strip()

        if not account_id:
            flash("Account ID is required.", "error")
            return render_template("activities/create_activity.html")

        if not category_id:
            flash("Category ID is required.", "error")
            return render_template("activities/create_activity.html")

        if not name:
            flash("Activity name is required.", "error")
            return render_template("activities/create_activity.html")

        if not goal:
            flash("Funding goal is required.", "error")
            return render_template("activities/create_activity.html")

        try:
            account_id = int(account_id)
            category_id = int(category_id)
            goal = float(goal)
        except ValueError:
            flash("Invalid numeric input.", "error")
            return render_template("activities/create_activity.html")

        success, message = controller.createActivity(
            account_id, category_id, name, desc, goal, start_date, end_date
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/create_activity.html")

# VIEW
@fundraising_activity_bp.route("/activities/view")
def view_activity():
    controller = view_fundraising_activity_controller()
    activities = controller.viewActivities()

    if not activities:
        flash("No activities found.", "error")
        return render_template("activities/view_activity.html")

    return render_template("activities/view_activity.html", activities=activities)


# UPDATE
@fundraising_activity_bp.route("/activities/update", methods=["GET", "POST"])
def update_activity():
    controller = update_fundraising_activity_controller()

    if request.method == "POST":
        activity_id = request.form.get("activityId", "").strip()
        name = request.form.get("name", "").strip()
        desc = request.form.get("desc", "").strip()
        goal = request.form.get("goal", "").strip()
        status = request.form.get("status", "").strip()

        if not activity_id:
            flash("Activity ID is required.", "error")
            return render_template("activities/update_activity.html")

        if not name:
            flash("Activity name is required.", "error")
            return render_template("activities/update_activity.html")

        try:
            activity_id = int(activity_id)
            goal = float(goal)
        except ValueError:
            flash("Invalid numeric input.", "error")
            return render_template("activities/update_activity.html")

        success, message = controller.updateActivity(
            activity_id, name, desc, goal, status
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/update_activity.html")


# DELETE
@fundraising_activity_bp.route("/activities/delete", methods=["GET", "POST"])
def delete_activity():
    controller = delete_fundraising_activity_controller()

    if request.method == "POST":
        activity_id = request.form.get("activityId", "").strip()

        if not activity_id:
            flash("Activity ID is required.", "error")
            return render_template("activities/delete_activity.html")

        success, message = controller.deleteActivity(activity_id)

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/delete_activity.html")
