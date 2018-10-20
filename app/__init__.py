from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Blablubb23'

from app import routes
