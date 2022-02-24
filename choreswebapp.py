from app import app, db
from app.models import User, ChoreList, ChoreProgress, ChoreAssignments
import time
from datetime import datetime


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ChoreList': ChoreList, 'ChoreProgress': ChoreProgress,
            'ChoreAssignments': ChoreAssignments}


@app.cli.command()
def scheduled():
    """Run Scheduled Jobs"""
    #  Move yesterdays assignment progresses to their appropriate table based on the status


    #  Ensure progress table is empty

    active_assignments = ChoreAssignments.query.filter_by(is_active='Yes').all()
    #  add active assignments to the progress table
    for c in active_assignments:
        db.session.add(ChoreProgress(chore_id=c.id, status='Incomplete', assigned_user=c.assigned_to.username,
                                     due_date=datetime.now(), value=c.assignment_id.value,
                                     description=c.assignment_id.description, occurrence=c.assignment_id.occurrence))

    db.session.commit()
    print('importing feeds...')
    time.sleep(5)
    print('Users: ', str(User.query.all()))
    print('DONE!!')

