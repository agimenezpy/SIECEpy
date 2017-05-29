from project.server import app
from project.utils import proxy


if __name__ == '__main__':
    app.register_blueprint(proxy, url_prefix="/salida")
    app.run(port=8000)
