from flask import Blueprint


test_routes = Blueprint('test_routes', __name__, url_prefix='/api')


@test_routes.route('/')
def index():
    return 'Index page'
