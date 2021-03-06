from flask import request, jsonify, current_app
# from flask_login import login_user, logout_user, current_user, login_required
# from werkzeug.urls import url_parse
# from mobilXpertenApp import db
from mobilXpertenApp.api import bp
from mobilXpertenApp.models import RepairDevice


@bp.route('/search')
def search():
    searchword = request.args.get('q', '')
    devices, total = RepairDevice.search(searchword, 1,
                            current_app.config['POSTS_PER_PAGE'])
    if (total > 0):
        response = [d.to_dict() for d in devices]
    else:
        response = {'result': 'No device found.'}
    return jsonify(response)

# @bp.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash('Kolla din email för vidare instruktioner.')
#         return redirect(url_for('login'))
#     return render_template('reset_password_request.html',
#                            title='Reset Password', form=form)


# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('login'))
#     return render_template('reset_password.html', form=form)


# @current_app.route('/')
# @current_app.route('/index')
# def index():
#     user = {'username': 'Henry'}
#     return render_template('index.html', title='Home', user=user)


# @current_app.route('/sallad')
# def sallad():
#     return "Hello, Sallad!"


# @current_app.route('/jimmie')
# def sallad():
#     return "Hello, Jimmie!"


# @current_app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)


# @bp.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
