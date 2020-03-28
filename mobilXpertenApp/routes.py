from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from mobilXpertenApp import app, db
from mobilXpertenApp.models import User, Device
from mobilXpertenApp.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from mobilXpertenApp.email import send_password_reset_email

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Kolla din email för vidare instruktioner.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Henry'}
    return render_template('index.html', title='Home', user=user)


@app.route('/sallad')
def sallad():
    return "Hello, Sallad!"

@app.route('/device/<id>', methods=['GET'])
def get_device(id):
    device = Device.query.get_or_404(id, description='There is no data with {}'.format(model))
    return jsonify(device)

@app.route('/device/<brand>/<model>', methods=['GET'])
def get_device_by_model(brand, model):
    device = Device.query.filter_by(model=model, brand=brand)\
        .first_or_404(description='There is no data with {}'.format(model))
    return jsonify(device)

@app.route('/device/<brand>', methods=['GET'])
def get_device_by_brand(brand):
    device = Device.query.filter_by(brand=brand).all()
    return jsonify(device)  

@app.route('/devices', methods=['GET'])
def get_devices():
    devices = Device.query.limit(100).all()
    return jsonify(devices)

@app.route('/devices', methods=['POST'])
def create_device():
    data = request.get_json() or {}
    if 'model' not in data or 'brand' not in data:
        return bad_request('must include model and brand fields')
    if Device.query.filter_by(username=data['model']).first():
        return bad_request('modelplease use a different username')
    device = Device()
    device.from_dict(data, new_device=True)
    db.session.add(device)
    db.session.commit()
    response = jsonify(device.to_dict())
    return response


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
    return render_template('login.html', title='Sign In', form=form)


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
