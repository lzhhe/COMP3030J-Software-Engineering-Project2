from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

utils = Blueprint('utils', __name__)  # department is name of blueprint


@utils.route('/', methods=['POST'])
def switch():

    return
