from flask import Blueprint, jsonify, abort, make_response, request 
from app import db
from app.models.rental import Rental
from app.routes.routes_helper import validate_model

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

## `POST /rentals/check-out`
@rentals_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()

    try:
        new_rental = Rental(customer_id=request_body["customer_id"],
                video_id=request_body["video_id"]
                )
    except KeyError as key_error:
        abort(make_response({"details":f"Request body must include {key_error.args[0]}."}, 400))

    db.session.add(new_rental)
    db.session.commit()

    rental_response = new_rental.to_dict()

    # assert response_body["videos_checked_out_count"] == 1
    # assert response_body["available_inventory"] == 0
    return jsonify(rental_response), 200


    # create a rental for the specific video and customer.
    # create a due date. The rental's due date is the seven days from the current date.

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