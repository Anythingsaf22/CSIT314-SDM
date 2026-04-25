from flask import Flask
from boundary.user_profile_routes import user_profile_bp
from boundary.fundraising_category_routes import fundraising_category_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(fundraising_category_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)