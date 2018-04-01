from flask import Flask
from config_local import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import controllers, models, view_models
