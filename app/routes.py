from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.video import Video
from app import db
from datetime import datetime
from app.models.customer import Customer

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------


# CREATE New Customer -- POST
@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    try:
        new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"],
                    registered_at=datetime.now()
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
    #return make_response(f"Customer #{customer.id} successfully deleted")

# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------
# CREATE New Video -- POST
@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    
    try:
        new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]
                    )
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))
    
    db.session.add(new_video)
    db.session.commit()
    
    video_response = new_video.to_dict()
    return jsonify(video_response),201

@videos_bp.route("", methods=["GET"])
def read_all_videos():
    video_query = Video.query
    videos = video_query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response),200

@videos_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = validate_model(Video, video_id)
    return video.to_dict()

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = validate_model(Video, video_id)
    request_body = request.get_json()

    try:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.commit()
    video_response = video.to_dict()

    return jsonify(video_response),200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = validate_model(Video, video_id)

    db.session.delete(video)
    db.session.commit()

    video_response = video.to_dict()
    return jsonify(video_response),200

# --------------------------------
# ----------- Helper Functions ---
# --------------------------------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    
    return model


