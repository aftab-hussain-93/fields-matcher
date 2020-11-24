from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
	file = FileField('Upload File', validators=[FileRequired(), FileAllowed(['csv',  'xls', 'xlsx'])])
	submit = SubmitField("Upload")