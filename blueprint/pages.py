# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for
from flask import abort, request, session, redirect
from jinja2 import TemplateNotFound

from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from common import db

import sys, traceback

pages = Blueprint('pages', __name__,
                template_folder='templates')

@pages.route('/')
def show():
    try:
        if 'username' in session:
            return redirect('/home')
        else:
            return render_template('login.html')
    except TemplateNotFound:
        abort(404)


@pages.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return redirect('/home')
        else:
            error = 'Invalid username/password'
            return render_template('login.html', error=error)
    else:
        return redirect('/home')

@pages.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('index'))

def valid_login(username, password):
    user = db.users.find_one({"username":username})
    print(user)
    if user == None:
        return False
    if pwd_context.verify(password, user["password"]):
        try:
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
        except:
            print "Exception in user code:"
            traceback.print_exc(file=sys.stdout)

        return True
    return False
