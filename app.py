from flask import Flask, render_template
from boundary.user_profile_routes import user_profile_bp
from boundary.fundraising_category_routes import fundraising_category_bp
from boundary.fundraising_activity_routes import fundraising_activity_bp
from boundary.user_account_routes import user_account_bp
from boundary.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    @app.route("/")
    def home():
        return render_template("home.html")

    app.register_blueprint(user_profile_bp)
    app.register_blueprint(fundraising_category_bp)
    app.register_blueprint(fundraising_activity_bp)
    app.register_blueprint(user_account_bp)
    app.register_blueprint(auth_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
