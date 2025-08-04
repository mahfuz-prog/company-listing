from flaskapp import db, bcrypt, serializer
from flaskapp.users.utils import user_filter
from flaskapp.users.db_models import User, UnverifiedUser
from flask_login import login_user, logout_user, current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskapp.users.forms import SignUp, SignIn, ForgotPassword, SetNewPassword
from flaskapp.users.messages import signup_email_verification, password_reset_varification

users = Blueprint('users', __name__)


# create account
@users.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
	if current_user.is_authenticated:
		flash(f'{current_user.username} You are already logged in!')
		return redirect(url_for('main.home'))
		
	form = SignUp(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		hashed_pass = bcrypt.generate_password_hash(password)
		user = UnverifiedUser(username=username, email=email, password=hashed_pass)
		db.session.add(user)
		db.session.commit()

		token = serializer.dumps(user.id)
		response = signup_email_verification(token, email)
		if response:
			flash('An email has been sent with email confirmation link. This link will expire after 20 minutes.', 'info')
			return redirect(url_for('users.sign_in'))
		else:
			flash(f"Mail dosen't send. Try again.")

	return render_template('users/signup.html', title='Create new account', form=form)


# signup email verification
@users.route('/verify-email/<token>')
def verify_email(token):
	user = UnverifiedUser.verify_email_token(token, max_age=1200)
	if user:
		verified_user = User(username=user.username, email=user.email, password=user.password)
		# add the verified user in User
		db.session.add(verified_user)

		# remove the user from UnverifiedUser
		db.session.delete(user)
		db.session.commit()

		flash(f'Account created for {user.username}.')
		return redirect(url_for('users.sign_in'))
	else:
		flash(f'Timeout or invalid token')
		return redirect(url_for('users.sign_up'))



# login
@users.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
	if current_user.is_authenticated:
		flash(f'{current_user.username} You are already logged in!')
		return redirect(url_for('main.home'))

	form = SignIn(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		user = user_filter(email=form.email.data)
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash(f'You are logged in as {user.username}', 'info')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Bad credentials', 'info')

	return render_template('users/signin.html', title='Sign in', form=form)


# logout user
@users.route('/log-out/')
@login_required
def log_out():
	username = current_user.username
	logout_user()
	flash(f'{username} successfully logged out.')
	return redirect(url_for('main.home'))

# reset passowrd
@users.route('/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
		
	form = ForgotPassword()
	if request.method == 'POST' and form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()
		token = serializer.dumps(user.id)
		status = password_reset_varification(token=token, email=email)
		if status:
			flash('An email has been sent with instructions for reset password')
			return redirect(url_for('users.sign_in'))
		else:
			flash('Something went wrong! please try again.')
	return render_template('/users/forgot-password.html', title='Password reset', form=form)

# verify reset password token
@users.route('/verify-reset/<token>', methods=['GET', 'POST'])
def verify_reset(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset(token, max_age=1200)
	if user:
		form = SetNewPassword()
		if request.method == 'POST' and form.validate_on_submit():
			hashed_pass = bcrypt.generate_password_hash(form.password.data)
			user.password = hashed_pass
			db.session.commit()
			flash('Password updated successfully.')
			return redirect(url_for('users.sign_in'))

		return render_template('users/reset-password.html', title='Set new password', form=form)
