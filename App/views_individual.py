from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint


@individual.route('/index')
def index():
    return render_template('individual/index.html')


@individual.route('/create')
def create():
    api_key = "392c5833885dafa9515b33b18592414e"
    api_security = "2e288d9ae8003f33cc1b58b5fd941663"
    wastes = None
    user = g.user
    if user is not None:
        wasteTypes = Waste.query.all()
        wastes = []
        for w in wasteTypes:
            wastes.append(w.wasteType)
    return render_template('individual/create.html', wastes=wastes, a1=api_security, a2=api_key)
