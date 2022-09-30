# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from apicontrolusohpc.controlhpc.controller import Controller
from apicontrolusohpc.controlhpc.processor import *
from apicontrolusohpc.controlhpc.loadconfig import get_admin

from apicontrolusohpc.auth import login_required
from apicontrolusohpc.utils import get_messages, fix_group, normalize_group

from datetime import date

from concurrent.futures import ThreadPoolExecutor

import time

views_bp = Blueprint('views', __name__)

@views_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        # recuperar entradas
        start_date = request.form["start_date"]
        if start_date == "":
            current_year = date.today().year
            start_date = "01/01/" + str(current_year)
        end_date = request.form["end_date"]
        if end_date == "":
            end_date = date.today().strftime("%d/%m/%Y")
        #group = request.form["group"]

        user = session['username']
        group = session['group']

        group = fix_group(group)
        #group = ""

        # cálculo
        start_time = time.time()
        new_controller = Controller()
        data = new_controller.match_date_range(start_date, end_date,group)
        owners = new_controller.get_group_users(group)
        results = {}
        print("--- %s data seconds ---" % (time.time() - start_time)) 
        start_time = time.time()
            
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = pool.submit(get_group_usage, group, data).result()
            users = pool.submit(get_group_users_usage, group, owners, data).result()


        #
        print("--- %s seconds ---" % (time.time() - start_time))
        return render_template('_views/index.html', data=results, group=normalize_group(group), messages=get_messages(), users=users, start_date=start_date, end_date=end_date)

    return render_template('_views/index.html')

@views_bp.route('/groups', methods=['GET','POST'])
@login_required
def index_group():
    user = session['username']
    admins = get_admin()
    if user not in admins:
        return redirect(url_for("index"))

    if request.method == "POST":
        #recuperar entradas
        start_date = request.form["start_date"]
        if start_date == "":
            current_year = date.today().year
            start_date = "01/01/" + str(current_year)

        end_date = request.form["end_date"]
        if end_date == "":
            end_date = date.today().strftime("%d/%m/%Y")

        #calculo
        start_time = time.time()
        new_controller = Controller()
        groups = new_controller.get_groups_names()
        data = new_controller.match_all_groups_date_range(start_date, end_date, groups)
        
        print("--- %s seconds data---" % (time.time() - start_time))
        start_time = time.time()

        results = get_groups_usages(data, groups)
        #
        print("--- %s seconds groups---" % (time.time() - start_time))
        return render_template('_views/results.html', data=results, start_date=start_date, end_date=end_date)

    return render_template('_views/index_group.html')



