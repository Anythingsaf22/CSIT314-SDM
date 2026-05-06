from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from control.search_fundraising_activity_controller import search_fundraising_activity_controller
from control.create_fundraising_activity_controller import create_fundraising_activity_controller
from control.view_fundraising_activity_controller import view_fundraising_activity_controller
from control.update_fundraising_activity_controller import update_fundraising_activity_controller
from control.delete_fundraising_activity_controller import delete_fundraising_activity_controller
from control.view_completed_activity_controller import view_completed_activity_controller
from control.search_completed_activity_controller import search_completed_activity_controller
from control.view_my_donation_controller import view_my_donation_controller
from control.search_my_donation_controller import search_my_donation_controller
from boundary.access_control import login_required, roles_required, FUNDRAISER, PLATFORM_MANAGEMENT


fundraising_activity_bp = Blueprint("fundraising_activity", __name__)


@fundraising_activity_bp.route("/activities/home")
def home():
    return redirect(url_for('fundraising_activity.list_activities'))

# LIST + SEARCH
@fundraising_activity_bp.route("/activities")
def list_activities():
    search_term = request.args.get("search", "")
    search_completed_term = request.args.get("searchCompleted", "")

    if "search" in request.args:
        if search_term.strip():
            searchController = search_fundraising_activity_controller()
            activities = searchController.searchActivities(search_term)
        else:
            flash("Activity name or description required.", "error")
            controller = view_fundraising_activity_controller()
            activities = controller.viewActivities()

    elif "searchCompleted" in request.args:
        if search_completed_term.strip():
            searchCompletedController = search_completed_activity_controller()
            activities = searchCompletedController.searchCompletedActivities(search_completed_term)
        else:
            flash("Activity name or description required.", "error")
            controller = view_completed_activity_controller()
            activities = controller.viewCompletedActivities()
    else:
        controller = view_fundraising_activity_controller()
        activities = controller.viewActivities()
    
    return render_template(
        "activities/list_activities.html",
        activities=activities,
        search_term=search_term,
        search_completed_term=search_completed_term
    )

# CREATE
@fundraising_activity_bp.route("/activities/create", methods=["GET", "POST"])
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
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
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
def update_activity():
    controller = update_fundraising_activity_controller()
    view_controller = view_fundraising_activity_controller()
    activity = None

    selected_activity_id = request.args.get("activityId", "").strip()
    if selected_activity_id:
        try:
            activity = view_controller.viewActivityById(int(selected_activity_id))
        except ValueError:
            flash("Invalid activity ID.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not activity:
            flash("Activity ID does not exist.", "error")

    if request.method == "POST":
        activity_id = request.form.get("activityId", "").strip()
        name = request.form.get("name", "").strip()
        desc = request.form.get("desc", "").strip()
        goal = request.form.get("goal", "").strip()
        status = request.form.get("status", "").strip()

        if not activity_id:
            flash("Activity ID is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        try:
            activity_id = int(activity_id)
        except ValueError:
            flash("Invalid activity ID.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        activity = view_controller.viewActivityById(activity_id)
        if not activity:
            flash("Activity ID does not exist.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not name:
            flash("Activity name is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not goal:
            flash("Funding goal is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        if not status:
            flash("Status is required.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        try:
            goal = float(goal)
        except ValueError:
            flash("Invalid numeric input.", "error")
            return render_template("activities/update_activity.html", activity=activity)

        success, message = controller.updateActivity(
            activity_id, name, desc, goal, status
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_activity.list_activities"))

        flash(message, "error")

    return render_template("activities/update_activity.html", activity=activity)


# DELETE
@fundraising_activity_bp.route("/activities/delete", methods=["GET", "POST"])
@roles_required(PLATFORM_MANAGEMENT, FUNDRAISER)
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

# VIEW COMPLETED ACTIVITIES
@fundraising_activity_bp.route("/activities/viewCompleted")
def view_completed_activities():
    search_term = request.args.get("search", "").strip()
    view_controller = view_completed_activity_controller()
    search_controller = search_completed_activity_controller()

    if "search" in request.args:
        if search_term:
            activities = search_controller.searchCompletedActivities(search_term)
        else:
            flash("Activity name or description required.", "error")
            activities = view_controller.viewCompletedActivities()
    else:
        activities = view_controller.viewCompletedActivities()

    if not activities:
        flash("No activities found.", "error")
        return render_template(
            "activities/view_completed_activity.html",
            activities=activities,
            search_term=search_term
        )

    return render_template(
        "activities/view_completed_activity.html",
        activities=activities,
        search_term=search_term
    )

# View and Search My Donations
@fundraising_activity_bp.route("/activities/myDonations")
@login_required
def view_my_donations():
    account_id = session.get("account_id")
    search_term = request.args.get("search", "").strip()
    viewController = view_my_donation_controller()
    searchController = search_my_donation_controller()
    donations = viewController.viewMyDonations(account_id)
    
    if "search" in request.args: 
        if search_term:
            donations = searchController.searchMyDonations(account_id, search_term)
        else:
            flash("Activity name or category required.", "error")

    if not donations:
        flash("No donations found.", "error")

    return render_template("activities/view_my_donations.html", donations=donations, search_term=search_term)
