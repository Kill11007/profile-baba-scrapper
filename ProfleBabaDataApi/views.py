# Django imports
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# Other imports
import os
import random
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def fetch_driver():

    # For proxy list of India from (https://docs.proxyscrape.com)
    proxy_url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=US&ssl=all&anonymity=all'
    proxies = requests.get(proxy_url).text.split('\r\n')[:-1]

    # Setting proxy settings
    proxy = random.choice(proxies)
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy,
        "ftpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }

    # To add user-agent---------------------------------------------------
    opts = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/74.0.3729.169 Safari/537.36'
    opts.add_argument("user-agent=user_agent")

    # Setting headless browser

    # Setting up driver
    opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opts.headless = False
    # chrome_options.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    my_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opts)

    # driver_path = Service(f'{os.path.dirname(os.path.abspath("chromedriver.exe"))}\\chromedriver.exe')
    # my_driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    # my_driver = webdriver.Chrome(service=driver_path, options=opts)

    return my_driver


try:
    # session for requests
    session = HTMLSession()

    # Getting driver
    driver = fetch_driver()
except Exception as e:
    print('error in driver :', e)

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


def for_google(query, no_of_records):
    base_url = 'https://www.google.com'
    driver.get(base_url)

    driver.find_element(By.CSS_SELECTOR, 'input[name="q"]').send_keys(query)

    driver.find_element(By.CSS_SELECTOR, 'span.mugnXc.Q0cixc').click()

    # select all links through soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Fetching all links
    links = soup.select('a.tHmfQe')

    for i in links[:no_of_records]:
        link = base_url + i['href']
        r = session.get(link).html

        # Name
        try:
            name = r.find('h2.qrShPb')[0].text
        except:
            name = ''

        # Address
        try:
            direction = r.find('span.LrzXr')[0].text
        except:
            direction = ''

        # Phone
        try:
            phone = r.find('span.LrzXr.zdqRlf.kno-fv')[0].text.replace(' ', '')
        except:
            phone = ''

        # Near Area
        try:
            near_area = r.find('a.V3h3K')[0].text
        except:
            near_area = ''

        # Rating
        try:
            rating = r.find('span.Aq14fc')[0].text
        except:
            rating = ''

        # Reviews
        try:
            review = r.find('span.hqzQac > span > a > span')[0].text.split(' ')[0]
        except:
            review = ''

        # Category
        try:
            category = r.find('span.YhemCb')[0].text
        except:
            category = ''

        # Website_link
        try:
            web_link = [i.attrs['href'] for i in r.find('div.QqG1Sd a.ab_button') if i.text == 'Website']
            if len(web_link) != 0:
                web_link = web_link[0]
            else:
                web_link = link
        except:
            web_link = link

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


def for_just_dial(query, cat, no_of_records):
    store_details = session.get('https://www.justdial.com/' + query).html.find('div.store-details')

    if len(store_details) < no_of_records:
        fetch_rec = len(store_details)
    else:
        fetch_rec = no_of_records

    # iterating the storeDetails
    for i in store_details[:fetch_rec]:
        url = i.find('span.jcn > a')[0].attrs['href']
        name = i.find('span.jcn > a')[0].attrs['title'].split(" in")[0]
        direction = i.find('span.cont_fl_addr')[0].text
        rating = i.find('span.green-box')[0].text
        review = i.find('p.newrtings > a > span.rt_count.lng_vote')[0].text.split(' ')[0]
        contact_list = i.find('span.mobilesv')
        phone = "".join([strings_to_num(j.attrs['class'][-1].split("-")[-1]) for j in contact_list])

        urls.append(url)
        names.append(name)
        directions.append(direction)
        phones.append(phone)
        ratings.append(rating)
        reviews.append(review)
        near_areas.append('')
        categories.append(cat)
        websites.append('https://www.justdial.com/')

    return


def my_scraper(input_state, input_cat, input_add, input_record_google, input_record_justdial):
    # Query to search
    query_google = f'{input_cat} in {input_add} {input_state} \n'
    query_jd = f'{input_state}/{input_cat}-in-{input_add}'.replace(' ', '-')

    # For JustDial
    for_just_dial(query_jd, input_cat, input_record_justdial)

    # For Google
    for_google(query_google, input_record_google)

    data_list = [{'url': url, 'name': name, 'address': direction, 'near_area': near_area, 'phone': phone,
                  'rating': rating, 'review': review, 'category': category, 'website': website}
                 for url, name, direction, near_area, phone, rating, review, category, website in
                 zip(urls, names, directions, near_areas, phones, ratings, reviews, categories, websites)]

    # Quit driver
    driver.quit()

    return data_list


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        try:
            query = request.query_params
            state = query['state']
            cat = query['cat']
            address = query['address']
            no_of_records_for_jd = query['nr_jd']
            no_of_records_for_google = query['nr_google']
            print('request', request)
            data = my_scraper(state, cat, address, int(no_of_records_for_jd), int(no_of_records_for_google))
            print('data', data)
            return Response(data)
        except Exception as e:
            status_code = 501
            message = "Internal Server Error"
            print(e)
            return JsonResponse({message: e}, status=status_code)

