from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.video import Video
from app import db
from app.routes.routes_helper import validate_model

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

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
