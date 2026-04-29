from flask import Blueprint, flash, redirect, render_template, request, url_for
from control.create_fundraising_category_controller import create_fundraising_category_controller
from control.view_fundraising_category_controller import view_fundraising_category_controller
from control.search_fundraising_category_controller import search_fundraising_category_controller
from control.update_fundraising_category_controller import update_fundraising_category_controller
from control.delete_fundraising_category_contorller import delete_fundraising_category_controller

fundraising_category_bp = Blueprint("fundraising_category", __name__)

@fundraising_category_bp.route("/categories/home")
def home():
    return redirect(url_for('fundraising_category.main_page'))

@fundraising_category_bp.route("/categories")
def main_page():
    search_term = request.args.get("search", "")
    controller = search_fundraising_category_controller()
    if "search" in request.args:
        if search_term.strip():
            categories = controller.searchCategories(search_term)
        else:
            flash("Category name needs to be provided.", "error")
            categories = []
    else:
            categories = 0
    return render_template(
        "categories/category_main_page.html", 
        categories=categories, 
        search_term = search_term
    )

@fundraising_category_bp.route("/categories/create", methods=["GET", "POST"])
def create_category():
    controller = create_fundraising_category_controller()

    if request.method == "POST":
        category_name = request.form.get("categoryName", "").strip()

        if not category_name:
            flash("Category name is required.", "error")
            return render_template("categories/category_create.html")
                
        success, message = controller.createFundraisingCategory(category_name)
        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_category.main_page"))

        flash(message, "error")

    return render_template("categories/category_create.html")

@fundraising_category_bp.route("/categories/view")
def view_category():
    controller = view_fundraising_category_controller()
    categories = controller.viewFundraisingCategory()
    if not categories:
        flash("No fundraising categories found.", "info")
        return render_template("categories/category_view.html")
    return render_template("categories/category_view.html", categories=categories)

@fundraising_category_bp.route("/categories/update", methods=["GET", "POST"])
def update_category():
    controller = update_fundraising_category_controller()

    if request.method == "POST":
        category_id = request.form.get("categoryId", "").strip()
        category_name = request.form.get("categoryName", "").strip()

        if not category_id:
            flash("Category ID is required.", "error")
            return render_template("categories/category_update.html")
        
        if not category_name:
            flash("Category name is required.", "error")
            return render_template("categories/category_update.html")
        
        success, message = controller.updateFundraisingCategory(
            category_id, 
            category_name
        )

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_category.main_page"))

        flash(message, "error")

    return render_template("categories/category_update.html")

@fundraising_category_bp.route("/categories/delete", methods=["GET", "POST"])
def delete_category():
    controller = delete_fundraising_category_controller()

    if request.method == "POST":
        category_id = request.form.get("categoryId", "").strip()

        if not category_id:
            flash("Category ID is required.", "error")
            return render_template("categories/category_delete.html")
        
        success, message = controller.deleteFundraisingCategory(category_id)

        if success:
            flash(message, "success")
            return redirect(url_for("fundraising_category.main_page"))
        
        flash(message, "error")

    return render_template("categories/category_delete.html")
