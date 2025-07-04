from flask_login import current_user
from flaskapp.companies.db_models import Company
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flaskapp.companies.utils import company_processor, all_category

companies = Blueprint('companies', __name__)


# get company by category
@companies.route('/<category>/')
def services(category):
	location = request.args.get('location', type=str)
	page = request.args.get('page', 1, type=int)

	# only 5 page accessable for not signed in user
	if page and page > 5 and not current_user.is_authenticated:
		flash(f'To access page {page}, you have to login!')
		return redirect(url_for('companies.services', category=category, page=1))
	
	if category not in all_category:
		flash(f"{category} does not exist! Redirected on 'software-development'")
		return redirect(url_for('companies.services', category='software-development'))

	# only for seo
	if location:
		if len(location) >= 35:
			flash('Location query parameter length should less than 35')
			return abort(404)

		total_counts = Company.query.filter(Company.services.icontains(category) & Company.locations.icontains(location)\
			& Company.headquarter.icontains(location))
		pagination = total_counts.paginate(page=page, per_page=20)
		companies = company_processor(pagination)

		if page == 1:
			title = f"Top 20+ { category.replace('-', ' ').capitalize() } agencies in { location }"
		else:
			title = f"Top { category.replace('-', ' ').capitalize() } agencies in { location }"

		return render_template('companies/companies_category.html', title=title, companies=companies, pagination=pagination,\
			category=category, location=location, total_counts=total_counts, categories=all_category)


	# if no location parameter
	total_counts = Company.query.filter(Company.services.icontains(category))
	pagination = total_counts.paginate(page=page, per_page=20)
	companies = company_processor(pagination)

	if page == 1:
		title = f"Top 20+ { category.replace('-', ' ').capitalize() } agencies"
	else:
		title = f"Top { category.replace('-', ' ').capitalize() } agencies"

	return render_template('companies/companies_category.html', title=title, companies=companies, pagination=pagination,\
		category=category, total_counts=total_counts, categories=all_category)




# search company by service
@companies.route('/search/', methods=["GET", "POST"])
def search():
	if request.method == 'POST':
		search_query = request.form.get('search')
		if search_query:
			search_query = search_query.replace(" ", "-").lower()

			pagination = Company.query.filter(Company.services.icontains(search_query)).limit(10).all()
			companies = company_processor(pagination)
			total_counts = Company.query.filter(Company.services.icontains(search_query)).count()
			return render_template('companies/search.html', title='Searched results', companies=companies,\
				total_counts=total_counts, search_query=search_query, categories=all_category)
		return abort(404)
	return abort(404)