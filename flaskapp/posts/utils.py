def post_processor(posts_lst):
	posts = []
	for item in posts_lst:
		# 'item.author' is already loaded due to eager loading
		# 'item.categories' is already loaded due to eager loading
		categories = [cat.category_name for cat in item.categories]

		x = {
			'id' : item.id,
			'featured_image': item.featured_image,
			'title': item.title,
			'excerpt' : item.excerpt, 
			'description' : item.description,
			'date_posted': item.date_posted,
			'user_id': item.user_id,
			'author' : item.author.username,
			'categories' : categories
		}

		posts.append(x)

	return posts