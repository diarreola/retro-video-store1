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

        videos_checked_out_count = len(Rental.query.filter_by(video.id).all())
        available_inventory = video.total_inventory - videos_checked_out_count

        if available_inventory == 0:
            abort(make_response({"message":f"Could not perform checkout"}, 400))
        
        new_rental = Rental(customer_id=request_body["customer_id"],
                video_id=request_body["video_id"]
                )
    except:
        abort(make_response({"message":f"Could not perform checkout"}, 400))

    video.video_checked_out_count += 1
    customer.video_checked_out_count += 1
    # db.session.add(customer)
    # db.session.add(video)
    db.session.add(new_rental)
    db.session.commit()


    rental_response = new_rental.to_dict()

    # add 
    rental_response["videos_checked_out_count"] = customer.videos_checked_out_count
    rental_response["available_inventory"] = available_inventory

    return jsonify(rental_response), 200


    # create a rental for the specific video and customer.

#     {
#   "customer_id": 122581016,
#   "video_id": 235040983,
#   "due_date": "2020-06-31",
#   "videos_checked_out_count": 2,
#   "available_inventory": 5
# }


#`POST /rentals/check-in`



## `GET /customers/<id>/rentals`




## `GET /videos/<id>/rentals`
