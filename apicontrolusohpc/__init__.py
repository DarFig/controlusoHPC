# -*- coding: utf-8 -*-

import os
from flask import Flask

from controlhpc.loadconfig import get_secret


def create_app():
    app = FLASK(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=get_secret()
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import views
    app.register_blueprint(views, views_bp)
    app.add_url_rule('/', endpoint='index')

    return app
