from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from wtforms import StringField, TextAreaField, SubmitField

class Contact(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email address', validators=[DataRequired(), Email(), Length(min=13, max=30)])
	subject = StringField('Subject', validators=[DataRequired(), Length(min=10, max=200)])
	description = TextAreaField('Message', validators=[DataRequired()])
	submit = SubmitField('Contact us')