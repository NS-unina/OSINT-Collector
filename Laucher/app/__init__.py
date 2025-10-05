import os
from flask import Flask
from app.views import views_bp


def create_app(config_class="app.configuration.DevelopmentConfig"):
    """
    Application factory function.
    Allows creating multiple Flask app instances with different configs.
    """
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(views_bp)

    return app


if __name__ == "__main__":


    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
