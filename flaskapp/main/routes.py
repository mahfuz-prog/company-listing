from flaskapp.main.forms import Contact
from flaskapp.main.message import contact_us_email
from flask import Blueprint, render_template, flash, request, redirect, url_for, make_response

main = Blueprint('main', __name__)

# homepage
@main.route('/')
def home():
	data = {'web_development' : 18002, 'data_science' : 3112, 'game_development' : 1136,\
	'animation' : 671, 'software_development' : 10784, 'blockchain' : 1109,\
	'digital_marketing' : 14641, 'ai' : 1523, 'ui' : 16630}

	return render_template('main/home.html', data=data)

# contact us page
@main.route('/contact-us/', methods=['GET', 'POST'])
def contact_us():
	form = Contact()
	if request.method == 'POST' and form.validate_on_submit():
		name = form.name.data
		email = form.email.data
		subject = form.subject.data
		description = form.description.data
		status = contact_us_email(name=name, email=email, subject=subject, description=description)
		if status:
			flash(f'{subject} - email successfully sent.')
			return redirect(url_for('main.contact_us'))
		else:
			flash('Something went wrong! please try again.')
	return render_template('main/contact.html', title='Contact us - webwaymark', form=form)