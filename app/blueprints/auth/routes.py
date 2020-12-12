import uuid
from flask import render_template, Blueprint, redirect, url_for, flash, request, session, current_app, jsonify
from .forms import RegisterForm, LoginForm #, RequestResetForm, PasswordResetForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.extensions import bcrypt, mongo, login_manager
from app.models import User
from bson.objectid import ObjectId

auth = Blueprint('auth',__name__)

@auth.route('/register.html', methods = ['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegisterForm()
	if request.method == "POST":
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(email = form.email.data, password_hash = hashed_password)
			user.add_user_to_db()
			flash(f'User {form.email.data} has been registered!', category='info')
			return redirect(url_for('auth.login'))
	return render_template('register.html', form= form)


@auth.route('/login.html', methods = ['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		log_user = User.login_valid(form.email.data, form.password.data)
		if log_user:
			login_user(log_user, remember=form.remember.data)
			next_page = request.args.get('next')
			session['user_id'] = log_user.public_id
			if not next_page or url_parse(next_page).netloc != '':
				return redirect(url_for('main.home'))
			else:
				return redirect(next_page)
		flash('Email or password incorrect please try again',  category='info')
		return redirect(url_for('auth.login'))
	return render_template('login.html', form= form)

@auth.route('/logout')
def logout():
	session.pop('user_id', None)
	logout_user()
	return redirect(url_for('main.home'))


@auth.route('/profile/user/<pub_id>')
@login_required
def profile(pub_id):
	return render_template("account.html")


@auth.route('/myfiles')
@login_required
def my_files():
	file_collection =  mongo.db.uploaded_files
	user_uploads = file_collection.find({'parent_file_oid': {"$exists": False}, 'user_id': current_user.public_id})
	result = []
	for f in user_uploads:
		updated_files = file_collection.find({"_id": {"$in": [ObjectId(ver) for ver in f['versions']]}})
		f['file_versions'] = updated_files
		result.append(f)
	return render_template('myfiles.html', user_uploads=result)

# @auth.route('/reset_password', methods = ['POST','GET'])
# def request_reset():
# 	if current_user.is_authenticated:
# 		flash('Please logout to reset password')
# 		return redirect(url_for('main.home'))
# 	form = RequestResetForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(email = form.email.data).first()
# 		send_reset_email(user)
# 		flash('Reset details have been sent over email. Please check to reset.')
# 		return redirect(url_for('auth.login'))
# 	return render_template('request_reset.html', form = form)


# @auth.route('/reset_password/<token>', methods = ['POST','GET'])
# def reset_token(token):
# 	if current_user.is_authenticated:
# 		return redirect(url_for('main.home'))
# 	user = User.verify_reset_token(token)
# 	if not user:
# 		flash('Invalid or Expired token')
# 		return redirect(url_for('auth.request_reset'))
# 	form = PasswordResetForm()
# 	if form.validate_on_submit():
# 		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
# 		user.password = hashed_password
# 		db.session.commit()
# 		flash('your password has been updated.')
# 		return redirect(url_for('auth.login'))
# 	return render_template('reset-token.html', form = form)