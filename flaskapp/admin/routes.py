import os
from flaskapp import db
from flask_login import current_user
from flaskapp.companies.forms import AddCompany
from flaskapp.admin.utils import save_img, admin_required
from flaskapp.posts.forms import NewPost, NewCategory, DeleteCategory, EditPost
from flaskapp.posts.db_models import Post, PostCategory, PostCategoryAssociation
from flaskapp.companies.db_models import Company, ServiceCategory, ServiceCategoryAssociation
from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app, abort
from flaskapp.companies.utils import all_category

admin = Blueprint('admin', __name__)

# admin dashboard
@admin.route('/')
@admin_required
def admin_panel():
	return render_template('admin/admin.html', title='Admin panel')


# show all admin post on admin dashboard
@admin.route('/all-posts/')
@admin_required
def all_posts():
	posts = Post.query.all()
	return render_template('admin/all_posts.html', title='All posts', posts=posts)


# create new post
@admin.route('/new-post/', methods=['POST', 'GET'])
@admin_required
def new_post():
	form = NewPost()
	categories = PostCategory.query.all()
	if request.method == 'POST' and form.validate_on_submit():
		selected_cat = request.form.getlist('option')

		img = save_img(form.featured_img.data, location='static/post_images')
		title = form.title.data.lower().replace(' ', '-')
		excerpt = form.excerpt.data
		description = form.description.data

		post = Post(featured_image=img, title=title, excerpt=excerpt, description=description, author=current_user)
		db.session.add(post)
		db.session.commit()

		# Get category objects corresponding to the names
		selected_category_objects = PostCategory.query.filter(
			PostCategory.category_name.in_(selected_cat)
		).all()

		# create relationship
		for cat_obj in selected_category_objects:
			post.categories.append(cat_obj)

		db.session.commit()
		flash('New post added', form.title.data)
		return redirect(url_for('admin.all_posts'))

	return render_template('admin/new_post.html', title='New Post', form=form, categories=categories)


# edit post
@admin.route('/edit-post/<post_id>', methods=['GET', 'POST'])
@admin_required
def edit_post(post_id):
	post = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).get(post_id)

	if not post:
		flash('Post not found!')
		return redirect(url_for('admin.all_posts'))


	form = EditPost(id=post_id)

	# handle post request
	if request.method == 'POST' and form.validate_on_submit():
		# change image
		if form.featured_img.data is not None:
			delete_img = os.path.join(current_app.root_path, 'static/post_images', post.featured_image)
			save_image = save_img(form.featured_img.data, location='static/post_images')
			post.featured_image = save_image
			os.remove(delete_img)

		# add new category to this post
		selected_category_names = request.form.getlist('selected_categories')
		# existing post category
		existing_category_objects = set(post.categories)

		# Get category objects corresponding to the names submitted in the form
		submitted_category_objects = set(PostCategory.query.filter(
			PostCategory.category_name.in_(selected_category_names)).all())

		# Categories to add: in submitted but not in existing
		to_add = submitted_category_objects - existing_category_objects
		for cat_obj in to_add:
			post.categories.append(cat_obj)

		# Categories to remove: in existing but not in submitted
		to_remove = existing_category_objects - submitted_category_objects
		for cat_obj in to_remove:
			post.categories.remove(cat_obj)

		# other post details
		post.title = form.title.data.lstrip().rstrip().replace(' ', '-').lower()
		post.excerpt = form.excerpt.data
		post.description = form.description.data
		db.session.commit()
		flash(f'{post.title} - successfully updated')
		return redirect(url_for('admin.edit_post', post_id=post_id))

	# handle get request
	# GET current post category
	post_categories = [cat.category_name for cat in post.categories]
	all_category_names = [cat.category_name for cat in PostCategory.query.all()]
	categories = [name for name in all_category_names if name not in post_categories]
	
	# set data to form
	form.title.data = post.title.replace('-', ' ').capitalize()
	form.excerpt.data = post.excerpt
	form.description.data = post.description

	title = post.title.replace('-', ' ').capitalize()
	return render_template('admin/edit_post.html', title=title, form=form, all_categories=categories,\
		post=post, post_categories=post_categories)


# add or delete post categories
@admin.route('/post-categories/', methods=['GET', 'POST'])
@admin_required
def post_categories():
	form_add = NewCategory()
	form_delete = DeleteCategory()
	categories = PostCategory.query.all()

	# create new category
	if request.method == 'POST' and form_add.validate_on_submit():
		if form_add.submit_add.data:
			category_name = form_add.category_name.data.strip().replace(' ', '-').lower()
			db.session.add(PostCategory(category_name=category_name))
			db.session.commit()
			flash(f'{category_name} - added')
			return redirect(url_for('admin.post_categories'))

	# delete existing category
	if request.method == 'POST' and form_delete.validate_on_submit():
		if form_delete.submit_delete.data:
			category_name = form_delete.category_name.data.strip().replace(' ', '-').lower()
			category_to_delete = PostCategory.query.filter_by(category_name=category_name).first()

			db.session.query(PostCategoryAssociation).filter_by(
				category_id=category_to_delete.id
			).delete(synchronize_session='fetch') # fetch ensures session is updated

			db.session.delete(category_to_delete)
			db.session.commit()
			flash(f'{category_name} - Deleted')
			return redirect(url_for('admin.post_categories'))

	return render_template('admin/post_categories.html', title='Post categories', categories=categories, form_add=form_add,\
		form_delete=form_delete)


# delete post
@admin.route('/delete-post/<post_id>')
@admin_required
def delete_post(post_id):
	post = Post.query.get(post_id)
	img = os.path.join(current_app.root_path, 'static/post_images', post.featured_image)
	os.remove(img)

	db.session.delete(post)
	db.session.commit()
	flash('Post deleted')
	return redirect(url_for('admin.all_posts'))


# add new company in listing
@admin.route('/add-company/', methods=['GET', 'POST'])
@admin_required
def add_company():
	form = AddCompany()
	if request.method == 'POST' and form.validate_on_submit():
		selected_cat = request.form.getlist('option')
		logo = save_img(form.logo.data, 'static/companies_logo')
		company_name = form.company_name.data
		services = form.services.data.split('|')
		locations = form.locations.data.split('|')
		social_links = form.social_links.data.split('|')
		company_website = form.company_website.data
		headquarter = form.headquarter.data
		description = form.description.data

		company = Company(
			company_name = company_name,
			services = f"{services}",
			description = description,
			locations = f'{locations}',
			social_links = f'{social_links}',
			company_website = company_website,
			logo = logo,
			headquarter = headquarter
			)

		db.session.add(company)
		db.session.flush()

		# Fetch all selected ServiceCategory objects in a single query
		selected_category_objects = ServiceCategory.query.filter(
			ServiceCategory.category.in_(selected_cat)
		).all()

		# Assign categories directly through the relationship property
		for cat_obj in selected_category_objects:
			company.categories.append(cat_obj)

		db.session.commit()
		flash('New company added')
		return redirect(url_for('admin.all_companies'))
	return render_template('/admin/add_company.html', title="Add new company", form=form, categories=all_category)


# delete company
@admin.route('/delete-company/<company_id>')
@admin_required
def delete_company(company_id):
	company = Company.query.get(company_id)
	title = company.company_name
	logo = os.path.join(current_app.root_path, 'static/companies_logo', company.logo)
	os.remove(logo)

	db.session.delete(company)
	db.session.commit()

	flash(f'{title} company deleted')
	return redirect(url_for('admin.all_companies'))