from flask import Blueprint, request, jsonify

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from models.opportunity import Opportunity

opportunity_bp = Blueprint(
    "opportunity",
    __name__
)

@opportunity_bp.route("/", methods=["POST"])
@login_required
def create_opportunity():

    data = request.json

    required_fields = [
        "name",
        "duration",
        "start_date",
        "description",
        "skills",
        "category",
        "future_opportunities"
    ]

    for field in required_fields:

        if not data.get(field):

            return jsonify({
                "error":
                f"{field} is required"
            }), 400

    opportunity = Opportunity(

        name=data["name"],

        duration=data["duration"],

        start_date=data["start_date"],

        description=data["description"],

        skills=data["skills"],

        category=data["category"],

        future_opportunities=data[
            "future_opportunities"
        ],

        max_applicants=data.get(
            "max_applicants"
        ),

        admin_id=current_user.id
    )

    db.session.add(opportunity)

    db.session.commit()

    return jsonify({
        "message":
        "Opportunity created successfully"
    }), 201

@opportunity_bp.route("/", methods=["GET"])
@login_required
def get_opportunities():

    opportunities = Opportunity.query.filter_by(
        admin_id=current_user.id
    ).all()

    result = []

    for opp in opportunities:

        result.append({

            "id": opp.id,

            "name": opp.name,

            "duration": opp.duration,

            "start_date": opp.start_date,

            "description": opp.description,

            "skills": opp.skills,

            "category": opp.category,

            "future_opportunities":
                opp.future_opportunities,

            "max_applicants":
                opp.max_applicants
        })

    return jsonify(result)

@opportunity_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_opportunity(id):

    opportunity = Opportunity.query.filter_by(
        id=id,
        admin_id=current_user.id
    ).first()

    if not opportunity:

        return jsonify({
            "error": "Opportunity not found"
        }), 404

    db.session.delete(opportunity)

    db.session.commit()

    return jsonify({
        "message":
        "Opportunity deleted successfully"
    })

@opportunity_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_opportunity(id):

    opportunity = Opportunity.query.filter_by(
        id=id,
        admin_id=current_user.id
    ).first()

    if not opportunity:

        return jsonify({
            "error": "Opportunity not found"
        }), 404

    data = request.json

    required_fields = [
        "name",
        "duration",
        "start_date",
        "description",
        "skills",
        "category",
        "future_opportunities"
    ]

    for field in required_fields:

        if not data.get(field):

            return jsonify({
                "error":
                f"{field} is required"
            }), 400

    opportunity.name = data["name"]

    opportunity.duration = data["duration"]

    opportunity.start_date = data["start_date"]

    opportunity.description = data["description"]

    opportunity.skills = data["skills"]

    opportunity.category = data["category"]

    opportunity.future_opportunities = data[
        "future_opportunities"
    ]

    opportunity.max_applicants = data.get(
        "max_applicants"
    )

    db.session.commit()

    return jsonify({
        "message":
        "Opportunity updated successfully"
    })