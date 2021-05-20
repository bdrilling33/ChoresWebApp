from app import app, db
from app.models import User, ChoreList, ChoreProgress, ChoreAssignments


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ChoreList': ChoreList, 'ChoreProgress': ChoreProgress,
            'ChoreAssignments': ChoreAssignments}


"""
<script>
 const btnDelete = document.querySelectorAll('.btn-delete');
 if(btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Are you sure you want to delete it?')){
                e.preventDefault();
            }
        });
    })
 }

</script>

"""