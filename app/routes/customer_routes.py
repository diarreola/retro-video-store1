from flask import Blueprint, jsonify, abort, make_response, request 
from app import db
from datetime import datetime
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from app.routes.routes_helper import validate_model, validate_num_queries

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
    # customers = customer_query.all()

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "name":
            customer_query = customer_query.order_by(Customer.name.asc())
        elif sort_query == "postal_code":
            customer_query = customer_query.order_by(Customer.postal_code.asc())
        elif sort_query == "registered_at":
            customer_query = customer_query.order_by(Customer.registered_at.asc())
        else:
            customer_query = customer_query.order_by(Customer.id.asc())

    count_query = request.args.get("count")  # check if count and page/ if only count, display all pages
    page_num_query = request.args.get("page_num")

    if validate_num_queries(count_query) and validate_num_queries(page_num_query):
        # need to check if count_query and page_num wuery are valid nums

        page = customer_query.paginate(page=int(page_num_query), per_page=int(count_query), error_out=False)
        customers = customer_query.all()

        customers_response = []

        for items in page.items:
            customers_response.append(items.to_dict())
        return jsonify(customers_response), 200

    if validate_num_queries(count_query) and not validate_num_queries(page_num_query):
        page = customer_query.paginate(per_page=int(count_query), error_out=False)
        customers = customer_query.all()
        customers_response = []

        for items in page.items:
            customers_response.append(items.to_dict())
        return jsonify(customers_response), 200


    customers = customer_query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

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

    customer_rentals = db.session.query(Rental).filter_by(customer_id=customer.id).all()

    if customer_rentals:
        for rental in customer_rentals:
            db.session.delete(rental)
        db.session.commit()

    db.session.delete(customer)
    db.session.commit()

    customer_response = customer.to_dict()
    return jsonify(customer_response),200

## `GET /customers/<id>/rentals` GET /customers/<id>/rentals
@customers_bp.route("/<id>/rentals", methods=["GET"])
def read_all_customer_rentals(id):
    customer = validate_model(Customer, id)
    customer_rentals = db.session.query(Rental).filter_by(customer_id=customer.id).all()
    video_query = customer_rentals.query(Video).filter_by(Rental.video_id).all()
    video_list = []
    for rental in customer_rentals:
        video = Video.query.get(rental.video_id)
        # video_list.append(video.to_dict())

    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "title":
            video_list = video_list.order_by(Video.title.asc())
        else:
            video_list = video_list.order_by(Video.id.asc())

    # for video in video_list:
    #     # video = Video.query.get(rental.video_id)
    #     video_list.append(video.to_dict())
    
    return jsonify(video_list), 200