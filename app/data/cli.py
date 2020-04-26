from app.data import data_bp
import csv
import os
from app.data.utils import extract_and_import_db, delete_data_db, delete_news_db


""" Flask CLI Commands (DATA) """
@data_bp.cli.command('add-data')
def add_data():
    extract_and_import_db()


@data_bp.cli.command('delete-all')
def delete_all():
    delete_data_db()
    delete_news_db()
