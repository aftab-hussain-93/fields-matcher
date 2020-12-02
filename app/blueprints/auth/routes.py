from flask import render_template, Blueprint, redirect, url_for, flash, request, session, current_app, jsonify
# from .forms import RegisterForm, LoginForm, RequestResetForm, PasswordResetForm
# from flask_login import current_user, login_user, logout_user, login_required
# from app import db, bcrypt, mail
# from .models import User
# from app.utils import get_user_files
# from werkzeug.urls import url_parse

auth = Blueprint('auth',__name__)

# @auth.route('/login.html', methods = ['POST','GET'])
# def login():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('main.home'))
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(email = form.email.data).first()
# 		if user and bcrypt.check_password_hash(user.password, form.password.data):
# 			login_user(user, remember = form.remember.data)
# 			next_page = request.args.get('next')
# 			session['username'] = user.username
# 			if not next_page or url_parse(next_page).netloc != '':
# 				return redirect(url_for('main.home'))
# 			else:
# 				return redirect(next_page)
# 		flash('Email or password incorrect please try again',  category='info')
# 		return redirect(url_for('auth.login'))
# 	return render_template('login.html', form= form)

# @auth.route('/register.html', methods = ['POST','GET'])
# def register():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('main.home'))
# 	form = RegisterForm()
# 	if request.method == "POST":
# 		print("request POST")
# 		if form.validate_on_submit():
# 			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
# 			user = User(email = form.email.data, username = form.username.data, password = hashed_password)
# 			db.session.add(user)
# 			db.session.commit()
# 			flash(f'User {form.username.data} has been registered!', category='info')
# 			return redirect(url_for('auth.login'))
# 	return render_template('register.html', form= form)


# @auth.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('main.home'))


# @auth.route('/profile/<user>')
# @login_required
# def profile(user):
# 	all_file_list = get_user_files(current_user)
# 	print(all_file_list)
# 	return render_template("account.html", files=all_file_list)

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