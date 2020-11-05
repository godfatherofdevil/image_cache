from flask import request, jsonify, current_app as app

from api.main import bp
from app.errors import BadRequest

search_terms = {"author", "camera", "tags"}


@bp.route("/api/search/<search_term>", methods=["GET", ])
def search_photos(search_term):
    if search_term not in search_terms:
        raise BadRequest(f"one of {search_terms} is required. got = {search_term}")

    cache = app.cache
    result = cache.get_term(search_term)

    return jsonify(result), 200

