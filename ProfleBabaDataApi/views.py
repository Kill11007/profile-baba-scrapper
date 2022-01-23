# Django imports
import time

from django.http import JsonResponse
from rest_framework.decorators import api_view
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Other imports
import os
import random
import urllib3
import requests
from bs4 import BeautifulSoup
from urllib3 import PoolManager
from requests_html import HTMLSession

# For proxy list of India from (https://docs.proxyscrape.com)
proxy_url = r'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=US&ssl=all&anonymity=all'
proxies = requests.get(proxy_url).text.split('\r\n')[:-1]
proxy = random.choice(proxies)


def fetch_driver():
    global proxies
    proxy = random.choice(proxies)

    # Setting proxy settings
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }

    # To add user-agent---------------------------------------------------
    opts = Options()
    # Setting up driver through env variable
    opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opts.headless = True
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    my_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opts)
    # my_driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=opts)

    return my_driver


# session for requests
session = HTMLSession()

# Getting driver
driver = fetch_driver()

# Headers for just Dial
header = {
    'Accept': '*/*',
    'cookie': 'TKY=6d4cda7ba15ba5ded3176c33b61267b4e82d50aad34b56ab3c7ba470e443c912; _abck=B2BD03FA2A626FBFD5697984DC832F40~-1~YAAQPUo5FwlCG+R9AQAA9lnq9geVWqK74XLky4hwTe0kHAZJDMkmXfQbWqXPV8lu1R1myaq5h74j6ZlUIYLFc3YbZbGfMajfZQoYsHmly0K3CH1RUiPpUCNl1b0Anm7BWgsXEZ+Gr/8qnV7LQqxZU9i8Vf0w5pPGKVCCkDTrqAxyOHsviYGGFU3Y4CDf5odsfsgbPOpXh4iBvEuPf1n5f0NRH8ypEFkWo+6hm4TUhpnMMSoQZcYN7/T167N0T6DTf0bWGcZqDrdz2ucY3zxXIMRf8ZX2U4a7ZL4VfqEBgFEhV1Y4VZnWwfWzYraokFILpN46+jIw4O3QEOHLPr38200vDHRrrXgTyncTYkv8ri8R38d9VlJC6O13agbkszUjKnKDcJluBKYBwMED~-1~-1~-1; _ctok=c0db6a9cb1a43b0b9a9ec5ffb88cdd49dc6235a77543330e5775afbc85d4943d; ak_bmsc=A5352C50CF860DD0B7C4226E5D089EE2~000000000000000000000000000000~YAAQLCEPF8ze8rd9AQAAJxjy9g5GtdYPipN3vJAWrXQ+3TqKoHN02j3j7zrhoqjubv/2BOUfdCaAhv2oW0q4VTNSfO05KkPbom0V5SO0KVPqEjI9bkpdUwgzGzyGOmK/+dF4LftTylJrG1MlqnDoDe0QoQ7zV8k6emRRx+3q0dfb1K6BW5bG1t/Iv+dY9dc5d1uonqUKXhWHtgsZOHMI+ielQxXQShiTp0WkfVDvt+PT2jS+ccQfSrPgePhN3nfPcuk3uLsnJjTqiNskDUFxfDnOnE8Y4NxBOY5fTtlJS8WDgZyWtzULdpKlGqO9rGZOwMUCZrKcsYhzgB07+wP6lfMdk6vlOUftDBnolj49JWmVlNoJbngpm5UDEyhvHdGAdTvwF+Ah+mQ2QddspwJvnCzTQerRh6JdeQ==; attn_user=logout; bm_mi=17863342B120E586ABC3FF83B6D0D933~7YGDThQe7Q8fq1WwBYjtPk27myCE96uXDvCM5kKxFW3QB5kTy2LHxOhkaciuGqrRcCKz6Zbhq9d/9m3kHtMCe6WejCT5x6A1SS2ugIJpcbbFyXAOR+svBAMsNyb79rPzKT8+rym9rFQenqH0EowfZMrJYpB4Vc9km1HZb4taNlw7P4QMal3mZb1Cw9vmZMt8F9mHWVbmiC38dVYO4cLg3NVTd5GTRwWlrb8Q4hlCYzk=; bm_sv=11DA979D7A0439D4C1268DA4FF7A3ADB~ezlXBQMhZps13vd0CuMdHPjpJagQdL9wwdH/JKK2TzSN5gU3rH6gNGfGRLYIHQXSYxSZmIIKbuaCt/N7MTeYycDxnoyVJruJOjpWx8qux34QC+n0OM8ZBv/x6BmP59im7Yd6HSyGj9z6xv5J+KPKQyQVnQ3+Y3XKQQxOAA91KOE=; bm_sz=C7FABE25C38754C832DF489AD7B1BA14~YAAQPUo5FwtCG+R9AQAA9lnq9g4QbALqk67Ir2oHKq2RidfEfp6BfcMYtrDDLNrRF+cvXsPtu3QAFbI8ontMNC7tLkpHoAgg/TfRQ5DqZyx6CX29TALl/1Rz9JXjApbGkzx2dBy/VoxfNSCqREjv5PFKNJiXr2lFmQ88Sg8/6VDnvSaQQCysqAL9mp64rSoEjikjzJC22eNCflPlHlwAJSRYc57ZusMkSl4EZdk1uBWoJ+xd818Sm06GPErQDmb+tu0YFEtUOUizGv9vhglf8xdv2qOCp/TtmVbHdyAZKJsBOiLWDw==~4601668~4470324; main_city=Mumbai; ppc=; Continent=AS; PHPSESSID=kjbj83ljbnc1nfh86bis6j8qf7'
}

# my_dict for df
urls, names, directions, near_areas, phones, ratings, reviews, categories, websites = [], [], [], [], [], [], [], [], []


# For phone no's
def strings_to_num(argument):
    switcher = {
        'dc': '+',
        'fe': '(',
        'hg': ')',
        'ba': '-',
        'acb': '0',
        'yz': '1',
        'wx': '2',
        'vu': '3',
        'ts': '4',
        'rq': '5',
        'po': '6',
        'nm': '7',
        'lk': '8',
        'ji': '9'
    }
    return switcher.get(argument, "")


def for_google(query, no_of_records=10):
    global driver, session
    print('inside this code...')

    base_url = 'https://www.google.com'
    driver.get(base_url)

    # Google search box
    driver.find_element(By.CSS_SELECTOR, 'input[name="q"]').send_keys(query)

    # Click on more items
    try:
        driver.find_element(By.CSS_SELECTOR, 'span.mugnXc.Q0cixc').click()
    except:
        driver.find_element(By.CSS_SELECTOR, 'span.wUrVib.OSrXXb').click()

    # select all links through soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Fetching all links
    records = soup.select('a.tHmfQe')

    if len(records) == 0:
        records = driver.find_elements(By.CSS_SELECTOR, 'div.eDIkBe > span:nth-child(1)')

    # Only select no of records given
    if len(records) < no_of_records:
        fetch_rec = len(records)
    else:
        fetch_rec = no_of_records

    # Looping over records
    for index, i in enumerate(records[:fetch_rec]):
        try:
            link = base_url + i['href']
            r = session.get(link).html
        except:
            r = soup

        # Name
        try:
            name = r.find('h2.qrShPb')[0].text
        except:
            try:
                driver.execute_script("arguments[0].click();", i)
                time.sleep(1.1)
                name = driver.find_elements(By.CSS_SELECTOR, 'h2.qrShPb')[0].text
            except:
                name = ''

        # Address
        try:
            direction = r.find('span.LrzXr')[0].text
        except:
            try:
                direction = driver.find_elements(By.CSS_SELECTOR, 'span.LrzXr')[0].text
            except:
                direction = ''

        # Phone
        try:
            phone = r.find('span.LrzXr.zdqRlf.kno-fv')[0].text.replace(' ', '')
        except:
            try:
                phone = driver.find_elements(By.CSS_SELECTOR, 'span.LrzXr.zdqRlf.kno-fv')[0].text
            except:
                phone = ''

        # Near Area
        try:
            near_area = r.find('a.V3h3K')[0].text
        except:
            try:
                near_area = driver.find_elements(By.CSS_SELECTOR, 'a.V3h3K')[0].text
            except:
                near_area = ''

        # Rating
        try:
            rating = r.find('span.Aq14fc')[0].text
        except:
            try:
                rating = driver.find_elements(By.CSS_SELECTOR, 'span.Aq14fc')[0].text
            except:
                rating = ''

        # Reviews
        try:
            review = r.find('span.hqzQac > span > a > span')[0].text.split(' ')[0]
        except:
            try:
                review = driver.find_elements(By.CSS_SELECTOR, 'span.hqzQac > span > a > span')[0].text.split(' ')[0]
            except:
                review = ''

        # Category
        try:
            category = r.find('span.YhemCb')[0].text
        except:
            try:
                category = driver.find_elements(By.CSS_SELECTOR, 'span.YhemCb')[0].text
            except:
                category = ''

        # Website_link
        try:
            web_link = [i.attrs['href'] for i in r.find('div.QqG1Sd a.ab_button') if i.text == 'Website']
            if len(web_link) != 0:
                web_link = web_link[0]
        except:
            try:
                web_link = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, 'div.QqG1Sd a.ab_button') if i.text == 'Website']
                if len(web_link) != 0:
                    web_link = web_link[0]
            except:
                web_link = ''

        websites.append(base_url)
        urls.append(web_link)
        names.append(name)
        directions.append(direction)
        phones.append(phone)
        near_areas.append(near_area)
        ratings.append(rating)
        reviews.append(review)
        categories.append(category)

    return


def for_just_dial(query, cat, no_of_records=10):
    global driver, session, header, proxy, proxies
    print('proxy :', proxy)
    full_url = 'https://www.justdial.com/' + query
    # http = PoolManager()
    # res = http.request('GET', full_url, headers=header, proxies=proxy)
    proxy = urllib3.ProxyManager(f'https://{proxies[0]}/', maxsize=10)
    res = proxy.request('GET', full_url, verify=False)
    print(res.data)

    # prox = '52.183.8.192:3128'
    # my_proxy = {'https': f'https://{prox}'}
    # full_url = 'https://www.justdial.com/' + query
    # print('full_url :', full_url)
    # print('my_proxy :', my_proxy)
    # r = session.request(method='GET', url=full_url, headers=header, proxies=my_proxy, verify=False)
    #
    # print('r.status_code :', r.status_code)
    # print('r.text :', r.text)
    #
    # store_details = r.html.find('div.store-details')
    # print('store_details :', len(store_details))
    #
    # if len(store_details) < no_of_records:
    #     fetch_rec = len(store_details)
    # else:
    #     fetch_rec = no_of_records
    #
    # # iterating the storeDetails
    # for i in store_details[:fetch_rec]:
    #     url = i.find('span.jcn > a')[0].attrs['href']
    #     name = i.find('span.jcn > a')[0].attrs['title'].split(" in")[0]
    #     direction = i.find('span.cont_fl_addr')[0].text
    #     rating = i.find('span.green-box')[0].text
    #     review = i.find('p.newrtings > a > span.rt_count.lng_vote')[0].text.split(' ')[0]
    #     contact_list = i.find('span.mobilesv')
    #     phone = "".join([strings_to_num(j.attrs['class'][-1].split("-")[-1]) for j in contact_list])
    #
    #     urls.append(url)
    #     names.append(name)
    #     directions.append(direction)
    #     phones.append(phone)
    #     ratings.append(rating)
    #     reviews.append(review)
    #     near_areas.append('')
    #     categories.append(cat)
    #     websites.append('https://www.justdial.com/')

    return


def my_scraper(input_state, input_cat, input_add, input_record_google=10, input_record_justdial=10):
    # Query to search
    query_google = f'{input_cat} in {input_add} {input_state} \n'
    query_jd = f'{input_state}/{input_cat}-in-{input_add}'.replace(' ', '-')

    # For JustDial
    # for_just_dial(query_jd, input_cat, input_record_justdial)
    print('going for google...')
    # For Google
    for_google(query_google, input_record_google)

    data_list = [{'url': url, 'name': name, 'address': direction, 'near_area': near_area, 'phone': phone,
                  'rating': rating, 'review': review, 'category': category, 'website': website}
                 for url, name, direction, near_area, phone, rating, review, category, website in
                 zip(urls, names, directions, near_areas, phones, ratings, reviews, categories, websites)]

    return data_list


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        try:
            query = request.query_params
            state = query['state'] if 'state' in query.keys() else ''
            cat = query['cat']
            address = query['address']
            no_of_records_for_jd = query['nr_jd'] if 'nr_jd' in query.keys() else 10
            no_of_records_for_google = query['nr_google'] if 'nr_google' in query.keys() else 10
            data = my_scraper(state, cat, address, int(no_of_records_for_jd), int(no_of_records_for_google))
            print('data', data)
            return JsonResponse(data, safe=False)
        except Exception as e:
            print('Exception in Api get request :', e)
            status_code = 501
            message = "Internal Server Error"
            return JsonResponse({message: e}, status=status_code)

