from app import app

if __name__ == '__main__':
    # import test routes
    from routes.test_routes import test_routes as test_routes_blueprint
    app.register_blueprint(test_routes_blueprint)

    app.run()
