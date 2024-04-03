from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, session, url_for, g, app, jsonify
from flask_babel import refresh
from sqlalchemy import and_, or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

utils = Blueprint('utils', __name__)  # department is name of blueprint


@utils.route('/switch_theme', methods=['POST'])
def switchTheme():
    theme = request.form.get('theme')
    session['theme'] = theme
    return jsonify({'success': True, 'message': 'Theme switched successfully'})


@utils.route('/switch_language', methods=['POST'])
def switchLanguage():
    language = request.form.get('language')
    session['language'] = language
    refresh()
    return jsonify({'success': True, 'message': 'Language switched successfully'})


def enum_to_string(enum):
    return enum.name.replace('_', ' ').title()


def string_to_enum(string):
    return string.replace(' ', '_').upper()
