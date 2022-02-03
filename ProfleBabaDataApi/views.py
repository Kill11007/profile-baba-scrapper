# Other imports
import os
import time
import random
import urllib3
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

# Django imports
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def fetch_driver():

    # For proxy list of India from (https://docs.proxyscrape.com)
    proxy_url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=' \
                '10000&country=US&ssl=all&anonymity=all'
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
    opts.add_argument("user-agent=user_agent")

    # Setting headless browser
    opts.headless = True

    # Setting up driver
    driver_path = Service("./chromedriver.exe")
    my_driver = webdriver.Chrome(service=driver_path, options=opts)

    return my_driver


# Getting driver
driver = fetch_driver()

# session for requests
session = HTMLSession()


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


def for_google(data_list, query, no_of_records=10):
    global driver

    base_url = 'https://www.google.com'
    driver.get(base_url)
    time.sleep(1.1)

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
        records = records[:len(records)].copy()
    else:
        records = records[:no_of_records].copy()

    print('no_of_records, len of records :', no_of_records, len(records))
    # Looping over records
    for i in records:
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
                web_link = [i.get_attribute('href') for i in driver.find_elements(
                    By.CSS_SELECTOR, 'div.QqG1Sd a.ab_button') if i.text == 'Website']
                if len(web_link) != 0:
                    web_link = web_link[0]
            except:
                web_link = ''

        data_list.append({'url': web_link, 'name': name, 'address': direction, 'near_area': near_area, 'phone': phone,
                          'rating': rating, 'review': review, 'category': category, 'website': base_url})

    return


def for_just_dial(data_list, query, no_of_records=10):
    base_url = 'https://www.justdial.com'
    driver.get(base_url)

    # Send Address
    ele = driver.find_element(By.CSS_SELECTOR, 'input#srchbx')
    ele.clear()
    ele.send_keys(query['cat'])
    ele.send_keys('\n')

    # Get cat Id
    cat_id = driver.current_url.split('/')[-1]

    # Making query for justdial
    query_jd = f"{base_url}/{query['state']}/{query['cat']} in {query['add']}/{cat_id}".replace(' ', '-')
    print('query_jd :', query_jd)

    store_details = session.get(query_jd).html.find('div.store-details.sp-detail')

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

        data_list.append({'url': url, 'name': name, 'address': direction, 'near_area': '', 'phone': phone,
                          'rating': rating, 'review': review, 'category': query['cat'], 'website': 'https://www.justdial.com/'})

    return


def my_scraper(input_state, input_cat, input_add, input_record_google, input_record_justdial):
    # Query to search
    data_list = []
    query_jd = {
        'state': input_state,
        'cat': input_cat,
        'add': input_add
    }

    # For JustDial
    try:
        print('going for JustDial...')
        for_just_dial(data_list, query_jd, input_record_justdial)
    except Exception as e:
        print('Exception in JustDial :', e)

    # For Google
    try:
        print('going for Google...')
        query_google = f'{input_cat} in {input_add} {input_state} \n'
        for_google(data_list, query_google, input_record_google)
    except Exception as e:
        print('Exception in Google :', e)

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
            data = my_scraper(state, cat, address, int(no_of_records_for_google), int(no_of_records_for_jd))
            print('data', data)
            # driver.quit()
            return JsonResponse(data, safe=False)
        except Exception as e:
            print('Exception in Api get request :', e)
