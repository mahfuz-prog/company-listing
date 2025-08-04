from flaskapp import db
from flask_login import current_user
from flaskapp.companies.db_models import Company, ServiceCategory
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flaskapp.companies.utils import company_processor

companies = Blueprint('companies', __name__)


# get company by category
@companies.route('/<string:category>/')
def services(category):
	# empty slug
	if not category:
		flash('Category required!')
		return abort(404)

	# invalid category
	category = ServiceCategory.query.filter_by(category_name=category).first()
	if not category:
		flash('Category not found!')
		return abort(404)


	page = request.args.get('page', 1, type=int)
	# only 5 page accessable for not signed in user
	if page and page > 5 and not current_user.is_authenticated:
		flash(f'To access page {page}, you have to login!')
		return redirect(url_for('companies.services', category=category.category_name, page=1))

	# query with eager loading
	pagination = category.companies.options(db.joinedload(Company.categories)).paginate(page=page, per_page=20)
	companies = company_processor(pagination)

	# seo
	if page == 1:
		title = f"Top 20+ { category.category_name.replace('-', ' ').capitalize() } agencies"
	else:
		title = f"Top { category.category_name.replace('-', ' ').capitalize() } agencies"

	all_categories = [c.category_name for c in ServiceCategory.query.all()]

	return render_template('companies/companies_category.html', title=title, companies=companies, pagination=pagination,\
		category=category.category_name, total_counts=pagination.total, categories=all_categories)


# The POST route can be used to redirect to the GET route for a cleaner URL
@companies.route('/search-post', methods=['POST'])
def search_post_handler():
	search_query = request.form.get('search')
	if search_query:
		# Redirect to the main search route with the query as a parameter
		# This is the Post/Redirect/Get pattern
		return redirect(url_for('companies.search', q=search_query))
	return redirect(url_for('companies.search'))


# search company by service
@companies.route('/search/', methods=["GET", "POST"])
def search():
	search_query = request.args.get('q', type=str)
	page = request.args.get('page', 1, type=int)

	if not search_query:
		flash('Please enter a search query.')
		abort(404)

	search_term = search_query.replace(" ", "-").lower()
	query = Company.query.options(db.joinedload(Company.categories)).join(Company.categories).filter(
		ServiceCategory.category_name.ilike(search_term)
	)

	pagination = query.paginate(page=page, per_page=20)
	companies = company_processor(pagination)

	all_categories = [c.category_name for c in ServiceCategory.query.all()]

	return render_template('companies/search.html', title='Searched results', companies=companies,\
		total_counts=pagination.total, search_query=search_term, categories=all_categories, pagination=pagination)