from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

blue = Blueprint('', __name__)  # cal_u is name of blueprint


@blue.route('/')
@blue.route('/main')
def main():
    return render_template('')





