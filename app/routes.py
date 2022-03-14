from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, AddChoreForm, EditChoreForm, AssignChoreForm, EditUserForm, \
    ChoreApproval
from flask_login import current_user, login_user, logout_user, login_required, user_needs_refresh
from app.models import User, ChoreList, ChoreAssignments, ChoreListSchema, UserListSchema, ChoreProgress
from werkzeug.urls import url_parse
from app import db, ma
import json
from datetime import datetime

@app.route('/')
@app.route('/index')
# @login_required
def index():

    choreprogress = ChoreProgress.query.all()
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    print(current_date)
    print(datetime.now())
    return render_template('index.html', title='Home', chores=choreprogress, date=current_date)


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
@app.route('/chore/<id>/delete', methods=['GET', 'POST'])
def delete_chore(id=None):

    delete_row = ChoreList.query.get(id)

    db.session.delete(delete_row)
    db.session.commit()
    flash('Chore {} has been deleted'.format(delete_row.description))

    return redirect(url_for('add_chore'))


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


@login_required
@app.route('/users', methods=['GET', 'POST'])
def users():

    user_list = User.query.all()

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=form.type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('{} is now a registered user!'.format(form.username.data))
        return redirect(url_for('users'))

    return render_template('users.html', form=form, users=user_list)


@app.route('/users/<id>/edit', methods=['GET', 'POST'])  # TODO finish this. add form, save changes etc
def user_edit(id=None):

    user = User.query.filter_by(id=id).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():

        user.username = form.username.data
        user.email = form.email.data
        user.user_type = form.user_type.data
        user.point_balance = int(form.point_balance.data)
        user.cash_balance = int(form.cash_balance.data)
        user.is_active = form.is_active.data
        user.approval_code = form.approval_code.data
        db.session.commit()
        flash('User {} has been updated'.format(form.username.data))
        return redirect(url_for('users'))
    print(form.errors)
    return render_template('edit_user.html', title='User Management', form=form)


# TODO: Add model and call this route to delete user from user list
@app.route('/users/<id>/delete', methods=['GET', 'POST'])
def user_chore(id=None):
    #  Doesnt actually delete, but marks as inactive.
    delete_row = User.query.get(id)
    delete_row.is_active = 'No'
    db.session.commit()
    flash('User {} has been inactivated'.format(delete_row.username))

    return redirect(url_for('users'))



@app.route('/chore_assignments/<id>/edit', methods=['GET', 'POST'])  # TODO finish this. add form, save changes etc
def assignment_edit(id=None):

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


################## API ROUTES #############################
@app.route('/api/get_chore_data', methods=['POST', 'GET'])
def get_chore_data():

    x = json.loads(request.data)
    chore_schema = ChoreListSchema()
    chore = ChoreList.query.filter_by(id=x['description']).first()
    output = chore_schema.dump(chore)
    print(output)

    return {'chore': output}
    # return redirect(url_for('assign_chore'))


@app.route('/api/get_user_data', methods=['POST', 'GET'])
def get_user_data():

    x = json.loads(request.data)
    user_schema = UserListSchema()
    user = User.query.filter_by(id=x['description']).first()
    output = user_schema.dump(user)

    return {'user': output}

@app.route('/chore_progress/<id>/completed', methods=['POST', 'GET'])
def choreComplete(id=None):

    chore = ChoreProgress.query.filter_by(id=id).first()
    print(chore)
    chore.status = 'Pending'
    db.session.commit()
    flash('Chore {} is pending approval'.format(chore.description))

    return redirect(url_for('index'))


@app.route('/chore_progress/<id>/approve', methods=['POST', 'GET'])
def choreApprove(id=None):
    print(id)
    chore = ChoreProgress.query.filter_by(id=id).first()
    form = ChoreApproval(obj=chore)

    if form.validate_on_submit():
        print(form.approved_by.data.username)
        approver = User.query.filter_by(username=form.approved_by.data.username).first()
        print(approver.approval_code)
        print(form.approval_code.data)
        if form.approval_code.data == approver.approval_code:

            chore.status = 'Completed'
            User.query.filter_by(username=chore.assigned_user).first().point_balance += chore.value
            db.session.commit()
            flash('Chore {} has been approved'.format(chore.description))
            return redirect(url_for('index'))
        else:
            flash('Approval Code is incorrect')
            form.approval_code.data = ''
    return render_template('approve_chore.html', title='Approve Chore', form=form)





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