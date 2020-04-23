from app.extensions import scheduler
from app.data.utils import extract_and_import_db
from datetime import datetime

# auto-update on interval
@scheduler.task('interval', id='extract_and_import_db', next_run_time=datetime.now(), hours=6, misfire_grace_time=900)
def auto():
    print("\n*** Auto updating the Google Sheet...")
    extract_and_import_db()
