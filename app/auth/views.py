from . import auth
from flask import render_template,redirect,url_for
from ..models import User
from .forms import RegistrationForm
from .. import db


@auth.route('/login')
def login():
    return render_template('auth/login.html')