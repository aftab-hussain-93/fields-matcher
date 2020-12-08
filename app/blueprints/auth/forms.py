from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
	email = StringField("Email Address",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(8,16)])
	submit = SubmitField("Sign In")
	remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
	email = StringField("Email Address",validators=[DataRequired(),Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(8)])
	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Register")

	def validate_email(self, email):
		user = User.get_by_email(self.email.data)
		if user:
			raise ValidationError("This email is already taken. Please use another one.")

# class RequestResetForm(FlaskForm):
# 	email = StringField("Email Address",validators=[DataRequired(),Email()])
# 	submit = SubmitField("Request Password Reset")

# 	def validate_email(self, email):
# 		user = User.query.filter_by(email = email.data).first()
# 		if not user:
# 			raise ValidationError("This email is not registered.")

# class PasswordResetForm(FlaskForm):
# 	password = PasswordField("Password",validators=[DataRequired(),Length(8)])
# 	confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
# 	submit = SubmitField("Reset Password")
