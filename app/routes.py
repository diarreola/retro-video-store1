from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.video import Video
from app import db
from datetime import datetime
from app.models.customer import Customer

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
# CREATE New Customer -- POST
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
    # customer_response = 
    return make_response(f"Customer {new_customer.name} successfully created", 201)








# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------
# CREATE New Video -- POST
@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"]
                    )

    db.session.add(new_video)
    db.session.commit()
    video_response = {"id": new_video.id,
                    "title":new_video.title,
                    "release_date":new_video.release_date,
                    "total_inventory":new_video.total_inventory
                    }
    return jsonify(video_response),201
    

