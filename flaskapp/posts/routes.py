import random
from flaskapp.posts.utils import post_processor
from flask import Blueprint, render_template, flash, redirect, url_for
from flaskapp.posts.db_models import Post, PostCategories, PostCategoryAssignment
from flaskapp.posts.featured import featured_post

posts = Blueprint('posts', __name__)


# all post
@posts.route('/')
def post():
	posts = Post.query.all()
	posts = post_processor(posts)
	cateories = PostCategories.query.all()
	featured = featured_post
	return render_template('posts/posts.html', title='All posts', posts=posts, cateories=cateories, featured=featured)


# only featured post
@posts.route('/featured-post/')
def read_featured():
	post = featured_post
	other_posts = Post.query.limit(20).all()
	other_posts = random.sample(other_posts, min(2, len(other_posts)))
	return render_template('posts/featured_post.html', title=featured_post['title'], post=featured_post, other_posts=other_posts)


# single post
@posts.route('/<title>')
def read_post(title):
	post = Post.query.filter_by(title=title).first()
	title = title.replace('-', ' ').capitalize()
	if post:
		association_list = PostCategoryAssignment.query.filter_by(post_id=post.id).all()
		categories = []
		for association in association_list:
			categories.append(PostCategories.query.get(association.category_id).category_name)

		all_cateories = PostCategories.query.all()
		all_cat_id = [x.id for x in all_cateories]
		post_category = [x.category_id for x in association_list]
		for id in all_cat_id:
			if id not in post_category:
				other_posts_assignment = PostCategoryAssignment.query.filter_by(category_id=id).limit(2).all()
				other_posts = [Post.query.get(post.post_id) for post in other_posts_assignment]
			else:
				other_posts = None

		return render_template('posts/single_post.html', title=title, post=post, categories=categories, other_posts=other_posts)
	else:
		flash('This post does not exist!')
		return redirect(url_for('posts.post'))


# blog by category
@posts.route('/category/<category>/')
def post_category_view(category):
	cat = PostCategories.query.filter_by(category_name=category).first()
	if cat:
		association_list = PostCategoryAssignment.query.filter_by(category_id=cat.id).all()
		posts = []
		for item in association_list:
			posts.append(Post.query.get(item.post_id))

		posts = post_processor(posts)
		cateories = PostCategories.query.all()
		title=category.replace('-', ' ').capitalize()
		featured = featured_post
		return render_template('posts/posts.html', title=title, posts=posts, cateories=cateories, featured=featured)
	else:
		flash('Category dose not exist.')
		return redirect(url_for('posts.post'))