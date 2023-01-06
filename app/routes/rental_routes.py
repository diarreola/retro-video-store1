from flask import Blueprint, jsonify, abort, make_response, request 
from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app.routes.routes_helper import validate_model

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

## `POST /rentals/check-out`
@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    try:
        customer = validate_model(Customer, request_body["customer_id"])
        video = validate_model(Video, request_body["video_id"])
        if video.total_inventory == 0:
            abort(make_response({"message":f"Could not perform checkout"}, 400))

        videos_checked_out = db.session.query(Rental).filter_by(video_id=video.id).all()

        available_inventory = video.total_inventory - len(videos_checked_out)
        if available_inventory == 0:
            abort(make_response({"message":f"Could not perform checkout"}, 400))
        
        new_rental = Rental(customer_id=request_body["customer_id"],
                video_id=request_body["video_id"]
                )
        
        customer.videos_checked_out_count += 1
    except KeyError as key_error:
        abort(make_response({"message":f"Could not perform checkout bc {key_error.args[0]}"}, 400))

    db.session.add(new_rental)
    db.session.add(customer)
    db.session.commit()

    rental_response = new_rental.to_dict()
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    available_inventory -= 1
    rental_response["available_inventory"] = available_inventory
    
    return jsonify(rental_response), 200


#`POST /rentals/check-in`



## `GET /customers/<id>/rentals`




## `GET /videos/<id>/rentals`
