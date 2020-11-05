from flask import Flask, jsonify
import threading

from api.main.before_start import before_start
from app.errors import BadRequest
from api.main.before_start import cache_manager


# error handlers
def bad_request(err):
    return jsonify({"error": str(err)}), 400


def unhandled(err):
    return jsonify({"error": str(err)}), 500


def handle_404(err):
    return jsonify({"error": str(err)}), 404


def create_app(env=None):
    app = Flask("image_server")
    app.register_error_handler(404, handle_404)
    app.register_error_handler(BadRequest, bad_request)
    app.register_error_handler(Exception, unhandled)
    # start the cache manager daemon
    cache_manager_daemon = threading.Thread(target=cache_manager)
    cache_manager_daemon.daemon = True
    cache_manager_daemon.start()
    cache = before_start()
    app.cache = cache
    register_blueprints(app)

    return app


def register_blueprints(app):
    from api.main import bp

    app.register_blueprint(bp)
