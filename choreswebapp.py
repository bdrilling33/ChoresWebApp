from app import app, db
from app.models import User, ChoreList, ChoreProgress, ChoreAssignments
import time


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ChoreList': ChoreList, 'ChoreProgress': ChoreProgress,
            'ChoreAssignments': ChoreAssignments}


@app.cli.command()
def scheduled():
    """Run Scheduled Jobs"""
    print('importing feeds...')
    time.sleep(5)
    print('Users: ', str(User.query.all()))
    print('DONE!!')

