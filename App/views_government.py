from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

government = Blueprint('government', __name__, url_prefix='/government')  # government is name of blueprint


@government.route('/')
def index():
    return render_template('government/index.html')
