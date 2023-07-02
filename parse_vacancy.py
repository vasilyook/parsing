import requests
import re
from bs4 import BeautifulSoup as BS

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
base_url = 'https://hh.ru/vacancy/81639879'


work = {
    'id': None,
    'company': {
        'id': None,
        'name': None,
        },
    'name': None,
    'published_date': None,
    'salary': None,
    'key_skills': None,
    'description': None,
    'contacts': None,
    'address': None
    }

# vacancy_id
work['id'] = int(re.findall('[0-9]+', base_url)[0])


def table(base_url):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = BS(request.content, 'html.parser')

        # company_address
        work['address'] = soup.find(attrs={'data-qa': 'vacancy-view-raw-address'}).get_text()

        # salary
        salary = soup.find(attrs={'data-qa': 'vacancy-salary'})
        work['salary'] = salary.get_text().replace(' ',' ')

        # key_skills
        key_skills = []
        hrefs = soup.find('div', class_='bloko-tag-list')
        skills = hrefs.find_all(attrs={'data-qa': 'bloko-tag__text'})
        for skill in skills:
            key_skills.append(skill.string)
        work['key_skills'] = key_skills

        # published_date
        date = soup.find('p', class_='vacancy-creation-time-redesigned')
        match = date.get_text().replace(' ',' ')
        match_res = re.split('Вакансия опубликована ', match)
        work['published_date'] = re.split(' в ', match_res[1])[0]

        # vacancy description
        description = soup.find('div', class_='g-user-content')
        work['description'] = description.get_text()

        # vacancy_name
        work['name'] = soup.find('div', class_='vacancy-title').h1.string

        # company_id, company_name
        company_data = soup.find('div', class_='vacancy-company-details')
        work['company']['id'] = int(re.findall('[0-9]+', company_data.span.a.get('href'))[0])
        work['company']['name'] = company_data.span.a.get_text().replace(' ',' ')

        return work

print(table(base_url))

