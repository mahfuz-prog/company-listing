import ast


countries = ['Albania', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Bahrain', 
	'Bangladesh', 'Belarus', 'Belgium', 'Bermuda', 'Bolivia', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 
	'Cameroon', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 'Cyprus', 'Denmark', 'Ecuador', 'Egypt', 
	'Estonia', 'Ethiopia', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 
	'Guatemala', 'Hungary', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 
	'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 
	'Lithuania', 'Luxembourg', 'Macedonia', 'Malaysia', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 
	'Montenegro', 'Morocco', 'Nepal', 'Netherlands', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 
	'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Serbia', 'Singapore', 
	'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Tunisia', 'Turkey', 
	'UAE', 'Uganda', 'Ukraine', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam']


def company_processor(company_lst):
	companies = []

	for company in company_lst:
		services = [c.category_name for c in company.categories]
		locations = ast.literal_eval(company.locations)
		social_links = ast.literal_eval(company.social_links)

		x = {
			'id' : company.id,
			'company': company.company_name,
			'services': services,
			'locations': locations,
			'social_links': social_links,
			'website' : company.company_website, 
			'logo' : company.logo,
			'headquater': company.headquarter
		}

		companies.append(x)

	return companies