import requests
import json
from bs4 import BeautifulSoup
from person import Person


def get_data(url):
    # get source code
    source_code = requests.get(url)
    # get plain text
    plain_text = source_code.text
    # pulling data
    soup = BeautifulSoup(plain_text, 'lxml')
    # init list person
    person_list = []
    # parse table info
    table = soup.find('table', {'class': 'views-table sticky-enabled cols-8'})

    if table is not None:
        for row in table.find_all('tr'):
            items = row.find_all('td')
            if len(items) > 0:
                photo = ''
                img_tag = items[0].find('img')
                if img_tag is not None:
                    photo = img_tag['src']
                name = items[1].string.strip()
                job_title = items[2].string.strip()
                email = items[3].string.strip()
                ext = items[4].string.strip()
                fax = items[5].string.strip()
                phone = items[6].string.strip()
                work_allocation = []
                if items[7] is not None:
                    p_tag = items[7].find_all('p')
                    for p in p_tag:
                        while p.find('br'):
                            # remove br tags
                            p.br.extract()
                        # add p tag contents to work allocation
                        work_allocation.append(p.contents)

                # put data into person object new_person
                new_person = Person(photo, name, job_title, email, ext, fax, phone, work_allocation)
                # add new_person to person list
                person_list.append(json.loads(new_person.to_json()))
        return person_list
    else:
        return None


# get data page by page
def spider_pages(start_page):
    page = start_page
    results = []
    while True:
        url = 'http://ministryoftextiles.gov.in/whos-who?page=' + str(page)
        person_list = get_data(url)
        if person_list is not None:
            results += person_list
            page += 1
        else:
            break
    print(json.dumps(results))


# execution
spider_pages(0)
