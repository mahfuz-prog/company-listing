import ast

all_category = ['metaverse-development', 'robotic-process-automation', 
	'maintenance-and-support', 'mobile-app-development', 'animation-and-multimedia', 
	'ar-and-vr-development', 'cloud-computing-services', 'web-hosting', 'bot-development', 
	'implementation-services', 'artificial-intelligence', 'testing-services', 'iot-development', 'advertising', 
	'engineering-services', 'devops', 'business-services', 'software-development', 
	'app-designing-ui-ux', 'big-data-and-bi', 'web-development', 'game-development', 'ecommerce-development', 
	'web-designing-ui-ux', 'writing-services', 'web3', 'blockchain-technology', 'digital-marketing', 
	'progressive-web-app'
]


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


def company_processor(lst):
	companies = []
	for item in lst:
		services = ast.literal_eval(item.services)
		locations = ast.literal_eval(item.locations)
		social_links = ast.literal_eval(item.social_links)

		x = {
			'id' : item.id,
			'company': item.company_name,
			'services': services,
			'locations': locations,
			'social_links': social_links,
			'website' : item.company_website, 
			'logo' : item.logo,
			'headquater': item.headquarter
		}

		companies.append(x)

	return companies