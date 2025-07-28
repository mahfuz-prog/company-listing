import random
from flaskapp import db
from flaskapp.posts.utils import post_processor
from flask import Blueprint, render_template, flash, redirect, url_for
from flaskapp.posts.db_models import Post, PostCategories, PostCategoryAssociation
from flaskapp.posts.featured import featured_post

posts = Blueprint('posts', __name__)


# all post
@posts.route('/')
def post():
	# Eager load author and categories to avoid N+1 in post_processor
	posts = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).all()

	posts = post_processor(posts)
	categories = PostCategories.query.all()
	featured = featured_post
	return render_template('posts/posts.html', title='All posts', posts=posts, categories=categories, featured=featured)


# only featured post
@posts.route('/featured-post/')
def read_featured():
	post = featured_post
	# Eager load
	other_posts = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).limit(20).all()
	
	other_posts = random.sample(other_posts, min(2, len(other_posts)))
	return render_template('posts/featured_post.html', title=featured_post['title'], post=featured_post, other_posts=other_posts)


# single post
@posts.route('/<title>')
def read_post(title):
	# Eager load
	post = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).filter_by(title=title).first()

	if not post:
		flash('This post does not exist!')
		return redirect(url_for('posts.post'))

	categories = [cat.category_name for cat in post.categories]
	other_posts = []

	# query other post from the same category except current post
	current_post_category_ids = [cat.id for cat in post.categories]
	# Eager load
	other_posts = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).join(PostCategoryAssociation).filter(
		PostCategoryAssociation.category_id.in_(current_post_category_ids),
		# Exclude the current post
		Post.id != post.id 
	).distinct().limit(3).all()

	return render_template('posts/single_post.html', title=title, post=post, categories=categories, other_posts=other_posts)


# blog by category
@posts.route('/category/<category>/')
def post_category_view(category):
	cat = PostCategories.query.filter_by(category_name=category).first()

	if not cat:
		flash('Category dose not exist.')
		return redirect(url_for('posts.post'))

	# Eager load
	posts_in_category = Post.query.options(
		db.joinedload(Post.author),
		db.selectinload(Post.categories)
	).join(Post.categories).filter(
		PostCategories.id == cat.id
	).distinct().order_by(Post.date_posted.desc()).all()

	posts = post_processor(posts_in_category)
	categories = PostCategories.query.all()
	title = category.replace('-', ' ').capitalize()
	featured = featured_post

	return render_template('posts/posts.html', title=title, posts=posts, categories=categories, featured=featured)