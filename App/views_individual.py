from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

individual = Blueprint('individual', __name__, url_prefix='/individual')  # individual is name of blueprint


@individual.route('/')
def index():
    return render_template('individual/dashboard.html')


@individual.route('/dashboard')
def dashboard():
    return render_template('individual/dashboard.html')


@individual.route('/todo')
def todo():
    return render_template('individual/todo.html')


@individual.route('/draw')
def draw():
    return render_template('individual/draw.html')
