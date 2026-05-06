from flask import Flask, render_template

from extensions import (
    db,
    bcrypt,
    login_manager
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "certifyme-intern-assessment-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

bcrypt.init_app(app)

login_manager.init_app(app)

from models.admin import Admin

@login_manager.user_loader
def load_user(user_id):

    return Admin.query.get(int(user_id))

from routes.auth_routes import auth_bp

from routes.opportunity_routes import opportunity_bp

app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

app.register_blueprint(
    opportunity_bp,
    url_prefix="/api/opportunities"
)

@app.route("/")
def home():

    return render_template("index.html")

with app.app_context():

    db.create_all()

if __name__ == "__main__":

    app.run(debug=True)