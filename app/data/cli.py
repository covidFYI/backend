from app.data import data_bp
import csv
import os
from app.extensions import mongo
from .utils import import_data_to_db


""" Flask CLI Commands (DATA) """
@data_bp.cli.command('add-data')
def add_data():
    import_data_to_db()


@data_bp.cli.command('delete-all')
def delete_all():
    entries = mongo.db.entries
    entries.delete_many({})

 
