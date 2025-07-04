from flaskapp import db

# companies table
class Company(db.Model):
	__tablename__ = 'companies'

	id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.String(40), unique=True)
	services = db.Column(db.String(150))
	description = db.Column(db.String(700))
	locations = db.Column(db.String(400))
	social_links = db.Column(db.String(150))
	company_website = db.Column(db.String(30), unique=True)
	logo = db.Column(db.String(16), unique=True)
	headquarter = db.Column(db.String(60))

	def __repr__(self):
		return f'<{self.company_name} | {self.services}| {self.locations} | {self.social_links} | \
		{self.company_website} | {self.logo} | {self.headquarter}>'


# categories
class ServiceCategory(db.Model):
	__tablename__ = 'service_categories'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	category = db.Column(db.String(30), unique=True, nullable=False)

	def __repr__(self):
		return f'<{self.category}>'


class ServiceCategoryAssociation(db.Model):
	__tablename__ = 'service_category_associations'

	companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), primary_key=True)

	def __repr__(self):
		return f'<com: {self.companies_id} | cat: {self.category_id}>'