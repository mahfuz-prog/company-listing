from flaskapp.posts.db_models import PostCategories, PostCategoryAssignment
def post_processor(lst):
	posts = []
	for item in lst:
		assignment_cat = PostCategoryAssignment.query.filter_by(post_id=item.id).all()
		categoris = []
		for cat in assignment_cat:
			category = PostCategories.query.get(cat.category_id).category_name
			categoris.append(category)

		x = {
			'id' : item.id,
			'featured_image': item.featured_image,
			'title': item.title,
			'excerpt' : item.excerpt, 
			'description' : item.description,
			'date_posted': item.date_posted,
			'user_id': item.user_id,
			'author' : item.author.username,
			'categories' : categoris
		}

		posts.append(x)

	return posts