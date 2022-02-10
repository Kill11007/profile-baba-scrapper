# Other imports
import time
import random
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor

# Django imports
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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
    my_driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=opts)

    return my_driver


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


def for_google(session, data_list, query, no_of_records=10):
    # Getting driver
    driver1 = fetch_driver()

    base_url = 'https://www.google.com'
    driver1.get(base_url)
    time.sleep(1.1)

    # Google search box
    driver1.find_element(By.CSS_SELECTOR, 'input[name="q"]').send_keys(query)

    # Click on more items
    try:
        driver1.find_element(By.CSS_SELECTOR, 'span.mugnXc.Q0cixc').click()
    except:
        driver1.find_element(By.CSS_SELECTOR, 'span.wUrVib.OSrXXb').click()

    # select all links through soup
    soup = BeautifulSoup(driver1.page_source, 'lxml')

    # Fetching all links
    records = soup.select('a.tHmfQe')

    if len(records) == 0:
        records = driver1.find_elements(By.CSS_SELECTOR, 'div.eDIkBe > span:nth-child(1)')

    # Only select no of records given
    if len(records) < no_of_records:
        records = records[:len(records)].copy()
    else:
        records = records[:no_of_records].copy()

    print('records found for google :', len(records))
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
                driver1.execute_script("arguments[0].click();", i)
                time.sleep(1.1)
                name = driver1.find_elements(By.CSS_SELECTOR, 'h2.qrShPb')[0].text
            except:
                name = ''

        # Address
        try:
            direction = r.find('span.LrzXr')[0].text
        except:
            try:
                direction = driver1.find_elements(By.CSS_SELECTOR, 'span.LrzXr')[0].text
            except:
                direction = ''

        # Phone
        try:
            phone = r.find('span.LrzXr.zdqRlf.kno-fv')[0].text.replace(' ', '')
        except:
            try:
                phone = driver1.find_elements(By.CSS_SELECTOR, 'span.LrzXr.zdqRlf.kno-fv')[0].text
            except:
                phone = ''

        # Near Area
        try:
            near_area = r.find('a.V3h3K')[0].text
        except:
            try:
                near_area = driver1.find_elements(By.CSS_SELECTOR, 'a.V3h3K')[0].text
            except:
                near_area = ''

        # Rating
        try:
            rating = r.find('span.Aq14fc')[0].text
        except:
            try:
                rating = driver1.find_elements(By.CSS_SELECTOR, 'span.Aq14fc')[0].text
            except:
                rating = ''

        # Reviews
        try:
            review = r.find('span.hqzQac > span > a > span')[0].text.split(' ')[0]
        except:
            try:
                review = driver1.find_elements(By.CSS_SELECTOR, 'span.hqzQac > span > a > span')[0].text.split(' ')[0]
            except:
                review = ''

        # Category
        try:
            category = r.find('span.YhemCb')[0].text
        except:
            try:
                category = driver1.find_elements(By.CSS_SELECTOR, 'span.YhemCb')[0].text
            except:
                category = ''

        # Website_link
        try:
            web_link = [i.attrs['href'] for i in r.find('div.QqG1Sd a.ab_button') if i.text == 'Website']
            if len(web_link) != 0:
                web_link = web_link[0]
        except:
            try:
                web_link = [i.get_attribute('href') for i in driver1.find_elements(
                    By.CSS_SELECTOR, 'div.QqG1Sd a.ab_button') if i.text == 'Website']
                if len(web_link) != 0:
                    web_link = web_link[0]
            except:
                web_link = ''

        data_list.append({'url': web_link, 'name': name, 'address': direction, 'near_area': near_area, 'phone': phone,
                          'rating': rating, 'review': review, 'category': category, 'website': base_url})

    # quit driver
    driver1.quit()
    return data_list


def for_just_dial(session, data_list, query, no_of_records=10):
    # Getting driver
    driver2 = fetch_driver()

    base_url = 'https://www.justdial.com'
    driver2.get(base_url)

    # Send Address
    ele = driver2.find_element(By.CSS_SELECTOR, 'input#srchbx')
    ele.clear()
    ele.send_keys(query['cat'])
    ele.send_keys('\n')

    # Get cat Id
    cat_id = driver2.current_url.split('/')[-1]

    # quit driver2
    driver2.quit()

    # Making query for justdial
    query_jd = f"{base_url}/{query['state']}/{query['cat']} in {query['add']}/{cat_id}".replace(' ', '-')
    print('query_jd :', query_jd)

    store_details = session.get(query_jd).html.find('div.store-details.sp-detail')

    if len(store_details) < no_of_records:
        store_details = store_details[:len(store_details)]
    else:
        store_details = store_details[:no_of_records]

    print('records found for justDial :', len(store_details))

    # iterating the storeDetails
    for i in store_details:
        try:
            url = i.find('span.jcn > a')[0].attrs['href']
        except:
            url = ''

        try:
            name = i.find('span.jcn > a')[0].attrs['title'].split(" in")[0]
        except:
            name = ''

        try:
            direction = i.find('span.cont_fl_addr')[0].text
        except:
            direction = ''

        try:
            rating = i.find('span.green-box')[0].text
        except:
            rating = ''

        try:
            review = i.find('p.newrtings > a > span.rt_count.lng_vote')[0].text.split(' ')[0]
        except:
            review = ''

        try:
            contact_list = i.find('span.mobilesv')
        except:
            contact_list = ''

        try:
            phone = "".join([strings_to_num(j.attrs['class'][-1].split("-")[-1]) for j in contact_list])
        except:
            phone = ''

        data_list.append({'url': url, 'name': name, 'address': direction, 'near_area': '', 'phone': phone,
                          'rating': rating, 'review': review, 'category': query['cat'], 'website': 'https://www.justdial.com/'})

    return data_list


def my_scraper(my_query):
    # session for requests
    session = HTMLSession()

    data_list = []
    query_google = f"{my_query['cat']} in {my_query['add']} {my_query['state']} \n"

    with ThreadPoolExecutor(max_workers=5) as pool:
        # For JustDial
        # print('going for JustDial...')
        try:
            pool.submit(for_just_dial, session, data_list, my_query, my_query['n_justdial'])
        except Exception as e:
            print('Exception in Google :', e)

        # For Google
        # print('going for Google...')
        try:
            pool.submit(for_google, session, data_list, query_google, my_query['n_google'])
        except Exception as e:
            print('Exception in Google :', e)

    return data_list


@api_view(['GET', 'POST'])
def snippet_list(request):
    try:
        print('...............................................Requested..........................................')
        if request.method == 'GET':
            query = request.query_params
            my_query = {
                'state': query['state'] if 'state' in query.keys() else '',
                'cat': query['cat'],
                'add': query['address'],
                'n_google': int(query['nr_jd']) if 'nr_jd' in query.keys() else 10,
                'n_justdial': int(query['nr_google']) if 'nr_google' in query.keys() else 10
            }

            data = my_scraper(my_query)
            # print('data', data)
            if len(data) == 0:
                print('--------data not found--------')
            else:
                print('----------data found----------')
            return JsonResponse(data, safe=False)
    except Exception as e:
        print('Exception in Api get request :', e)
