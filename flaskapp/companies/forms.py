from flask_wtf import FlaskForm
from flaskapp.companies.db_models import Company
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, URL, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, BooleanField

class AddCompany(FlaskForm):
	logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png'], 'Images only! jpg, png')])
	company_name = StringField('Company name', validators=[DataRequired(), Length(min=3, max=40)])
	services = StringField('Services seperated by |', validators=[DataRequired(), Length(min=3, max=150)])
	locations = StringField('Locations seperated by |', validators=[DataRequired(), Length(min=10, max=400)])
	social_links = StringField('Social media seperated by |', validators=[DataRequired(), Length(min=10, max=150)])
	company_website = StringField('Company website', validators=[DataRequired(), Length(min=3, max=30), URL(message='Example: https://www.demo.com')])
	headquarter = StringField('Headquarter', validators=[DataRequired(), Length(min=10, max=60)])
	description = TextAreaField('Description', validators=[DataRequired(), Length(min=30, max=700)])
	option = BooleanField('Option')
	submit = SubmitField('Add company')


	def validate_logo(self, logo):
		if not logo.data:
			raise ValidationError('Please select a logo')

	def validate_company_name(self, company_name):
		company = Company.query.filter_by(company_name=company_name.data).first()
		if company:
			raise ValidationError('Company already registered')

	def validate_company_website(self, company_website):
		company = Company.query.filter_by(company_website=company_website.data).first()
		if company:
			raise ValidationError('This website already exists in our company list')

	def validate_option(self, option):
		if not option.data:
			raise ValidationError('Please select a category')