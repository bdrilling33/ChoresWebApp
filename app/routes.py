from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddChoreForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, ChoreList
from werkzeug.urls import url_parse
from app import db


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
def chore_edit(id):
    chore = ChoreList.query.filter_by(id=id).first()
    form = AddChoreForm(chore.id)
    if form.validate_on_submit():
        print(form.value.data)

    return render_template('edit_chore', form=form, title='Edit Chore')


@app.route('/chore/<id>/delete', methods=['GET', 'POST'])
def delete_chore(id=None):

    delete_row = ChoreList.query.get(id)

    db.session.delete(delete_row)
    db.session.commit()
    flash('Chore {} has been deleted'.format(delete_row.description))

    return redirect(url_for('add_chore'))
