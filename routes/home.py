import os
from flask import Blueprint, send_from_directory, redirect

home_bp = Blueprint('home_bp', __name__)

@home_bp.route("/")
def index():
    return redirect("/home")

@home_bp.route("/home")
def landing_page():
    try:
        print("Serving landing.html from /home route")
        return send_from_directory(os.path.join(os.path.dirname(__file__), '../templates'), 'landing.html')
    except Exception as e:
        return f"<h1>Error loading landing page:</h1><p>{e}</p>", 500