from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from control.add_favourite_controller import add_favourite_controller
from control.view_favourite_controller import view_favourite_controller
from control.search_favourite_controller import search_favourite_controller
from boundary.access_control import login_required, roles_required, DONOR
