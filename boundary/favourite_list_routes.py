from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.add_favourite_list_controller import add_favourite_list_controller
from control.view_favourite_list_controller import view_favourite_list_controller
from control.search_favourite_list_controller import search_favourite_list_controller
from boundary.access_control import login_required, roles_required, DONOR

favourite_bp = Blueprint("favourite_list", __name__)

