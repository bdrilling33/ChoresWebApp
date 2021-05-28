from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, AddChoreForm, EditChoreForm, AssignChoreForm
from flask_login import current_user, login_user, logout_user, login_required, user_needs_refresh
from app.models import User, ChoreList, ChoreAssignments, ChoreListSchema
from werkzeug.urls import url_parse
from app import db, ma
import json

@app.route('/')
@app.route('/index')
@login_required
def index():

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The advenders movie is cool!'
        },
        {
            'author': {'username': 'Brice'},
            'body': "I'm starting to get the hang of this!"
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', Title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=form.type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_chore', methods=['GET', 'POST'])
# @login_required
def add_chore():
    form = AddChoreForm()
    chores = ChoreList.query.all()
    if form.validate_on_submit():

        chore = ChoreList(description=form.description.data, occurrence=form.occurrence.data,
                          created_by_id=form.created_by.data.id, value=int(form.value.data))
        db.session.add(chore)
        db.session.commit()
        flash('Chore {} has been added'.format(form.description.data))
        return redirect(url_for('add_chore'))
    return render_template('add_chore.html', title='Add Chore', form=form, chores=chores)


@app.route('/chore/<id>/edit', methods=['GET', 'POST'])
def chore_edit(id=None):

    chore = ChoreList.query.filter_by(id=id).first()
    form = EditChoreForm(obj=chore)
    if form.validate_on_submit():

        chore.description = form.description.data
        chore.occurrence = form.occurrence.data
        chore.created_by_id = form.created_by.data.id
        chore.value = int(form.value.data)
        print(chore.value)
        print(form.value.data)
        print('edit submitted')
        db.session.commit()
        flash('Chore {} has been updated'.format(form.description.data))
        return redirect(url_for('add_chore'))
    print(form.errors)
    return render_template('edit_chore.html', title='Edit Chore', form=form)

# TODO: Add model and call this route to delete chore from chore list
# @app.route('/chore/<id>/delete', methods=['GET', 'POST'])
# def delete_chore(id=None):
#
#     delete_row = ChoreList.query.get(id)
#
#     db.session.delete(delete_row)
#     db.session.commit()
#     flash('Chore {} has been deleted'.format(delete_row.description))
#
#     return redirect(url_for('add_chore'))

# TODO: Load Chore Edit to a modal.  use this route to fill modal form with selected row data
# @app.route('/api/chorelist', methods=['POST', 'GET'])
# def get_chore_list():
#     chore_schema = ChoreListSchema()
#     chore = ChoreList.query.filter_by(id=request.form['id']).first()
#     output = chore_schema.dump(chore)
#     form = AddChoreForm(obj=chore)
#     print(output)
#     # return render_template('edit_chore.html', form=form)
#     # #return jsonify({'chore': output})
#     return jsonify({'chore': output})


@app.route('/chore_assignments', methods=['POST', 'GET'])
def assign_chore():

    form = AssignChoreForm()
    assigned_chores = db.session.query(ChoreAssignments, ChoreList, User).join(ChoreList, ChoreList.id ==
        ChoreAssignments.chore_id).join(User, ChoreAssignments.assigned_by_id == User.id).\
            order_by(ChoreAssignments.assigned_user_id.asc(), ChoreList.occurrence.asc()).all()

    if form.validate_on_submit():
        chore = ChoreAssignments(chore_id=form.assign_chore.data.id, assigned_user_id=form.assign_to.data.id,
                                            assigned_by_id=form.assigned_by.data.id)
        db.session.add(chore)
        db.session.commit()
        flash('Chore {} has been assigned to {}'.format(form.assign_chore.data.description,
                                                        form.assign_to.data.username))

        return redirect(url_for('assign_chore'))

    return render_template('assign_chores.html', form=form, assigned_chores=assigned_chores)


@app.route('/api/get_chore_data', methods=['POST', 'GET'])
def get_chore_data():

    x = json.loads(request.data)
    chore_schema = ChoreListSchema()
    chore = ChoreList.query.filter_by(id=x['description']).first()
    output = chore_schema.dump(chore)
    print(output)

    return {'chore': output}
    # return redirect(url_for('assign_chore'))

