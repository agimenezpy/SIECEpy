# Flask Application

import os
from flask import Flask, render_template, request
from flask.helpers import url_for
from flask_flatpages import FlatPages
from project.model import CLIMATE_MODELS

__all__ = ['BASE_DIR', 'ROOT_DIR', 'app']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.dirname(BASE_DIR))
app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(ROOT_DIR, "public"))
app_settings = os.getenv('APP_SETTINGS',
                         'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)
pages = FlatPages(app)


@app.context_processor
def inject_static_url():
    return dict(STATIC_URL=app.static_url_path,
                INDEX_URL=url_for('index'),
                PATH_URL=request.path)


@app.route("/")
def index():
    return render_template('index.html', page={})


@app.route("/<path:path>.html")
def content(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    extra = {"page": page}
    if path in CLIMATE_MODELS:
        extra["model"] = CLIMATE_MODELS[path]
    if path == "equipo":
        extra["model"] = [subpage for subpage in pages if subpage.path.startswith("perfil")]
    return render_template(template, **extra)
