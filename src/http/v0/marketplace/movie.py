from flask import jsonify, request, Blueprint, flash
from src.sdk.cache import ingest, mint, manager, cursor_db, DESCENDING
from werkzeug.utils import secure_filename
from src.sdk.exception import InvalidRequest
from src.sdk.util import extract_extension
from src.sdk.constants import NODE_URI, API_VERSION, ALLOWED_VIDEO_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS, UPLOAD_FOLDER
from bson.objectid import ObjectId

movie_ = Blueprint("movie", __name__)


def _process_files(files):
    """
    Validate uploaded files and store it into local filesystem
    :param files: Files
    :return tuple: (image, video)
    """
    if 'image' not in files or 'video' not in files:
        raise InvalidRequest("Not valid media to process provided")

    image = files.get('image')  # Uploaded image poster
    video = files.get('video')  # Uploaded video media file

    # TODO validate image ratio

    if extract_extension(image) not in ALLOWED_IMAGE_EXTENSIONS:
        raise InvalidRequest('Invalid image format')
    if extract_extension(video) not in ALLOWED_VIDEO_EXTENSIONS:
        raise InvalidRequest('Invalid video format')

    # Pass it a filename and it will return a secure version of it
    # https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.utils.secure_filename
    image_filename = secure_filename(image.filename)
    video_filename = secure_filename(video.filename)
    # Store files into local filesystem
    image.save(UPLOAD_FOLDER, image_filename)
    video.save(UPLOAD_FOLDER, video_filename)

    return image, video


def _sanitize_internals(entry):
    """
    Re-struct response cleaning internal data
    :param entry: MovieScheme dict
    :return MovieScheme dict with cleaned and sanitized fields
    """

    # Sanitize uri to get handled by proxy
    # Set paths for assets and nav
    entry["_id"] = str(entry["_id"])
    entry["path"] = f"/{entry['_id']}"
    posters = entry["resource"]["image"]
    new_image_path = f"{NODE_URI}/{API_VERSION}/marketplace/proxy{entry['path']}"
    entry["posters"] = {
        i: f"{new_image_path}?arg={v}" for i, v in posters["index"].items()
    }

    # Clean not public data
    del entry["hash"]  # remove needed pre-processing field
    del entry["resource"]
    return entry


@movie_.route("profile", methods=["GET"])
def profile():
    _id = request.args.get("id")
    # Get current latest minted movies
    minted_nft, _ = mint.frozen({}, {"cid": 1, "_id": False})
    movie = manager.get(cursor_db, _filter={"_id": ObjectId(_id)})
    return jsonify(_sanitize_internals(movie))


@movie_.route("recent", methods=["GET"])
def recent():
    order_by = request.args.get("order", DESCENDING)
    limit = request.args.get("limit", 10)

    # Get current latest minted movies
    minted_nft, _ = mint.frozen({}, {"cid": 1, "_id": False})
    minted_nft_limited = list(minted_nft.limit(limit))  # slice response
    mapped_cid = map(lambda x: x.get("cid"), minted_nft_limited)

    # Parse erc1155 metadata
    # Get "in-relation" hash from ingested metadata
    metadata_for_cid, _ = ingest.frozen({"hash": {"$in": tuple(mapped_cid)}})
    metadata_for_cid.sort([("_id", order_by)])  # sort descending by date
    movies_meta = map(_sanitize_internals, metadata_for_cid)
    return jsonify(list(movies_meta))


@movie_.route("create", methods=["POST"])
def create():
    metadata = request.args
    # Pre-processing uploaded files
    image, video = _process_files(request.files)
