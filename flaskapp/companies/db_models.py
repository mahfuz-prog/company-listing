from flaskapp import db

# company table
class Company(db.Model):
	__tablename__ = 'company'

	id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.String(40), unique=True)
	description = db.Column(db.String(700))
	locations = db.Column(db.String(400))
	social_links = db.Column(db.String(150))
	company_website = db.Column(db.String(30), unique=True)
	logo = db.Column(db.String(16), unique=True)
	headquarter = db.Column(db.String(60))

	categories = db.relationship(
		'ServiceCategory',
		secondary='service_category_association',
		lazy='selectin',
		backref=db.backref('companies', lazy='dynamic'),
	)

	def __repr__(self):
		return f'<{self.company_name} | {self.locations} | {self.social_links} | \
		{self.company_website} | {self.logo} | {self.headquarter}>'


# categories
class ServiceCategory(db.Model):
	__tablename__ = 'service_category'

	id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(30), unique=True, nullable=False)

	def __repr__(self):
		return f'<{self.category_name}>'


# association table
class ServiceCategoryAssociation(db.Model):
	__tablename__ = 'service_category_association'

	company_id = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), primary_key=True)

	def __repr__(self):
		return f'<com: {self.company_id} | cat: {self.category_id}>'