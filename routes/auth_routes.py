from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

from extensions import db, bcrypt
from models.admin import Admin

auth_bp = Blueprint("auth", __name__)

serializer = URLSafeTimedSerializer("supersecretkey")

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not all([
        full_name,
        email,
        password,
        confirm_password
    ]):
        return jsonify({
            "error": "All fields are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    if password != confirm_password:
        return jsonify({
            "error": "Passwords do not match"
        }), 400

    existing_user = Admin.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Account already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    admin = Admin(
        full_name=full_name,
        email=email,
        password=hashed_password
    )

    db.session.add(admin)

    db.session.commit()

    return jsonify({
        "message": "Account created successfully"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")

    password = data.get("password")

    remember = data.get("remember", False)

    admin = Admin.query.filter_by(
        email=email
    ).first()

    if not admin:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    valid_password = bcrypt.check_password_hash(
        admin.password,
        password
    )

    if not valid_password:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    login_user(admin, remember=remember)

    return jsonify({
        "message": "Login successful",
        "admin": {
            "id": admin.id,
            "name": admin.full_name,
            "email": admin.email
        }
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():

    logout_user()

    return jsonify({
        "message": "Logged out successfully"
    })

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.json

    email = data.get("email")

    admin = Admin.query.filter_by(
        email=email
    ).first()

    if admin:

        token = serializer.dumps(
            email,
            salt="password-reset"
        )

        reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

        # Reset link generated internally

    return jsonify({
        "message":
        "If the email exists, a reset link has been generated."
    })

@auth_bp.route("/reset-password/<token>", methods=["GET"])
def reset_password(token):

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=3600
        )

        return jsonify({
            "message": "Valid reset link",
            "email": email
        })

    except:

        return jsonify({
            "error": "Reset link expired or invalid"
        }), 400