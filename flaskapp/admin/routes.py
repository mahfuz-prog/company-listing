import os
from flaskapp import db
from flaskapp.companies.forms import AddCompany
from flask_login import current_user
from flaskapp.admin.utils import save_img, admin_required
from flaskapp.posts.forms import NewPost, NewCategory, DeleteCategory, EditPost
from flaskapp.posts.db_models import Post, PostCategories, PostCategoryAssignment
from flaskapp.companies.db_models import Company, ServiceCategory, ServiceCategoryAssociation
from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app, abort
from flaskapp.companies.utils import all_category

admin = Blueprint('admin', __name__)

# admin dashboard
@admin.route('/')
@admin_required
def admin_panel():
	return render_template('admin/admin.html', title='Admin panel')


# create new post
@admin.route('/new-post/', methods=['POST', 'GET'])
@admin_required
def new_post():
	form = NewPost()
	categories = PostCategories.query.all()
	if request.method == 'POST' and form.validate_on_submit():
		selected_cat = []
		for value in request.form.getlist('option'):
			selected_cat.append(value)

		img = save_img(form.featured_img.data, location='static/post_images')
		title = form.title.data.lower().replace(' ', '-')
		excerpt = form.excerpt.data
		description = form.description.data

		post = Post(featured_image=img, title=title, excerpt=excerpt, description=description, author=current_user)
		db.session.add(post)
		db.session.commit()

		for item in selected_cat:
			cat = PostCategories.query.filter_by(category_name=item).first()
			db.session.add(PostCategoryAssignment(post_id=post.id, category_id=cat.id))
			
		db.session.commit()
		flash('New post added', form.title.data)
		return redirect(url_for('admin.all_posts'))

	return render_template('admin/new_post.html', title='New Post', form=form, categories=categories)


# edit post
@admin.route('/edit-post/<id>', methods=['GET', 'POST'])
@admin_required
def edit_post(id):
	post = Post.query.get(id)
	if post:
		form = EditPost(id=id)
		post_categories = []
		for cat in PostCategoryAssignment.query.filter_by(post_id=id).all():
			post_categories.append(PostCategories.query.get(cat.category_id).category_name)

		all_categories = PostCategories.query.all()
		categories = []
		for category in all_categories:
			if category.category_name not in post_categories:
				categories.append(category.category_name)

		if request.method == 'POST' and form.validate_on_submit():
			if form.featured_img.data is not None:
				delete_img = os.path.join(current_app.root_path, 'static/post_images', post.featured_image)
				save_image = save_img(form.featured_img.data, location='static/post_images')
				post.featured_image = save_image
				os.remove(delete_img)

			if form.add_category.data:
				selected_cat = []
				for value in request.form.getlist('add_category'):
					selected_cat.append(value)

				for item in selected_cat:
					cat = PostCategories.query.filter_by(category_name=item).first()
					db.session.add(PostCategoryAssignment(post_id=id, category_id=cat.id))

			if form.remove_category.data:
				selected_cat = []
				for value in request.form.getlist('remove_category'):
					selected_cat.append(value)

				if selected_cat != post_categories:
					for item in selected_cat:
						cat = PostCategories.query.filter_by(category_name=item).first()
						association_delete = PostCategoryAssignment.query.filter_by(post_id=id, category_id=cat.id).all()
						for association in association_delete:
							db.session.delete(association)

			post.title = form.title.data.lstrip().rstrip().replace(' ', '-').lower()
			post.excerpt = form.excerpt.data
			post.description = form.description.data
			db.session.commit()
			flash(f'{post.title} - successfully updated')
			return redirect(url_for('admin.edit_post', id=id))

		elif request.method == 'GET':
			form.title.data = post.title.replace('-', ' ').capitalize()
			form.excerpt.data = post.excerpt
			form.description.data = post.description
	else:
		flash('Post not found!')
		return redirect(url_for('admin.all_posts'))

	title = post.title.replace('-', ' ').capitalize()
	return render_template('admin/edit_post.html', title=title, form=form, all_categories=categories,\
		post=post, post_categories=post_categories)


# show all admin post on admin dashboard
@admin.route('/all-posts/')
@admin_required
def all_posts():
	posts = Post.query.all()
	return render_template('admin/all_posts.html', title='All posts', posts=posts)


# add or delete post categories
@admin.route('/post-categories/', methods=['GET', 'POST'])
@admin_required
def post_categories():
	form_add = NewCategory()
	form_delete = DeleteCategory()
	categories = PostCategories.query.all()

	if request.method == 'POST' and form_add.validate_on_submit():
		if form_add.submit_add.data:
			category_name = form_add.category_name.data.replace(' ', '-').lower()
			db.session.add(PostCategories(category_name=category_name))
			db.session.commit()
			flash(f'{category_name} - added')
			return redirect(url_for('admin.post_categories'))

	if request.method == 'POST' and form_delete.validate_on_submit():
		if form_delete.submit_delete.data:
			category_name = form_delete.category_name.data.replace(' ', '-').lower()
			category = PostCategories.query.filter_by(category_name=category_name).first()

			association_delete = PostCategoryAssignment.query.filter_by(category_id=category.id).all()
			for association in association_delete:
				db.session.delete(association)

			db.session.delete(category)
			db.session.commit()
			flash(f'{category_name} - Deleted')
			return redirect(url_for('admin.post_categories'))

	return render_template('admin/post_categories.html', title='Post categories', categories=categories, form_add=form_add,\
		form_delete=form_delete)


# delete post
@admin.route('/delete-post/<id>')
@admin_required
def delete_post(id):
	post = Post.query.get(id)
	img = os.path.join(current_app.root_path, 'static/post_images', post.featured_image)
	os.remove(img)

	association_delete = PostCategoryAssignment.query.filter_by(post_id=id).all()
	for association in association_delete:
		db.session.delete(association)

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
		selected_cat = []
		for value in request.form.getlist('option'):
			selected_cat.append(value)

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
		db.session.commit()

		for item in selected_cat:
			cat = ServiceCategory.query.filter_by(category=item).first()
			db.session.add(ServiceCategoryAssociation(companies_id=company.id, category_id=cat.id))
		db.session.commit()
		flash('New company added')
		return redirect(url_for('admin.all_companies'))

	return render_template('/admin/add_company.html', title="Add new company", form=form, categories=all_category)


# delete company
@admin.route('/delete-company/<id>')
@admin_required
def delete_company(id):
	company = Company.query.get(id)
	title = company.company_name
	logo = os.path.join(current_app.root_path, 'static/companies_logo', company.logo)
	os.remove(logo)

	association_delete = ServiceCategoryAssociation.query.filter_by(companies_id=id).all()
	for association in association_delete:
		db.session.delete(association)

	db.session.delete(company)
	db.session.commit()

	flash(f'{title} company deleted')
	return redirect(url_for('admin.all_companies'))