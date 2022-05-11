# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

views_bp = Blueprint('views', __name__)

@views_bp.route('/', methods=['GET'])
def index():
    return render_template('_views/index.html')



