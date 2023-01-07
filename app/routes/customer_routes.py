from flask import Blueprint, jsonify, abort, make_response, request 
from app import db
from datetime import datetime
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from app.routes.routes_helper import validate_model

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# CREATE New Customer -- POST
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    try:
        new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"]
                    # registered_at=datetime.now()
                    )
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(new_customer)
    db.session.commit()

    customer_response = new_customer.to_dict()
    return jsonify(customer_response), 201

@customers_bp.route("", methods=["GET"])
def read_all_customers():
    customer_query = Customer.query
    customers = customer_query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def read_one_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    return customer.to_dict()

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    request_body = request.get_json()
    # customer = Customer.from_dict(request_body)
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.commit()
    customer_response = customer.to_dict()

    return jsonify(customer_response),200
    
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = validate_model(Customer, customer_id)

    db.session.delete(customer)
    db.session.commit()

    customer_response = customer.to_dict()
    return jsonify(customer_response),200

## `GET /customers/<id>/rentals` GET /customers/<id>/rentals
@customers_bp.route("/<id>/rentals", methods=["GET"])
def read_all_customer_rentals(id):
    customer = validate_model(Customer, id)

    # get video ids from rental model based on the customer id
    customer_rentals = db.session.query(Rental).filter_by(customer_id=customer.id).all()
    video_list = []
    for rental in customer_rentals:
        # video = db.session.query(Video).filter_by(video_id=rental.video_id)
        video = Video.query.get(rental.video_id)
        video_list.append(video.to_dict())
    
    # get video details from video model
    return jsonify(video_list), 200

# List the videos a customer currently has checked out

# CHECK: if customer does not exist!
# empty list of no video checked out
# response
# [
#     {
#         "release_date": "Wed, 01 Jan 1958 00:00:00 GMT",
#         "title": "Vertigo",
#         "due_date": "Thu, 13 May 2021 19:27:47 GMT",
#     },
#     {
#         "release_date": "Wed, 01 Jan 1941 00:00:00 GMT",
#         "title": "Citizen Kane",
#         "due_date": "Thu, 13 May 2021 19:28:00 GMT",
#     }
# ]
# 