from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.video import Video
from app import db
from datetime import datetime
from app.models.customer import Customer

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"],
                    registered_at=datetime.now()
                    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(f"Customer {new_customer.name} successfully created", 201)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"],
                    registered_at=datetime.now()
                    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(f"Customer {new_customer.name} successfully created", 201)

