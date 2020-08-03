# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import Flask, session, app, request
from main import index
from location import location

app = Flask(__name__, template_folder='view', static_url_path='', static_folder='static')

app.secret_key = 'selkjfoiasdasdwspvkmoivejfoiwjfoijiofj'

app.register_blueprint(index.main_blue)
app.register_blueprint(location.location_blue)

app.run(host='0.0.0.0', port = 5000)