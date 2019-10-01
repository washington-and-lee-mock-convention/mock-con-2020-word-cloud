import os
import connexion
from connexion.resolver import RestyResolver

API_PORT = os.environ.get('API_PORT', 8080)

def setup_app():
    app = connexion.AioHttpApp(__name__, specification_dir='swagger/')
    app.add_api('api.spec.yaml', resolver=RestyResolver('api'))
    return app

if __name__ == '__main__':
    app = setup_app()
    app.run(port=API_PORT)