# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from controlhpc.controller import Controller
from controlhpc.processor import *

views_bp = Blueprint('views', __name__)

@views_bp.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        # recuperar entradas
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        
        # cálculo
        new_controller = Controller()
        data = new_controller.match_date_range(start_date, end_date)
        results = get_groups_usages(data)

        #
        return render_template('_views/respuesta.html', data=results)

    return render_template('_views/index.html')


