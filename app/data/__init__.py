from flask import Blueprint

data_bp = Blueprint('data', __name__)

from app.data import controller
from app.data import cli
from app.data import schedule
