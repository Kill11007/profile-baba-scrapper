# Django imports
from django.http import JsonResponse
from rest_framework.decorators import api_view
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Other imports
import os
import random
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def fetch_driver():

    # For proxy list of India from (https://docs.proxyscrape.com)
    proxy_url = r'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=' \
                r'US&ssl=all&anonymity=all'
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
                 'Chrome/96.0.4664.110 Safari/537.36'
    opts.add_argument("user-agent=user_agent")

    # Setting up driver through env variable
    opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opts.headless = True
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    my_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opts)

    return my_driver


# session for requests
session = HTMLSession()

# Getting driver
driver = fetch_driver()

# Headers for just Dial
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'ppc=; ppc=; _ctok=3a5b4b0786bc93bc313b6c59051b4a1170107d89d12a9f2e37a8bdd9e0057afe; _ga=GA1.2.2009095260.1638019562; _fbp=fb.1.1638019561638.450925677; vfdisp=%7B%22011PXX11.XX11.190131111444.J3V2%22%3A%221024%22%7D; TKY=008ade917391af8a466c4a4ec56fc20d6d5673aca5606f1ec1792e325886542e; akcty=Delhi; attn_user=logout; bm_sz=AD15D3C4A0CE0B6173ECB71C4E27013A~YAAQJCEPFyspmfB9AQAAl4c99g4fVDHcf133JKL7qacaNXp2D42j43oqK1awV1yj3EVRYhjAbP6uHr1PIy6SwfK6AgCfCBlMh55pVEqcabJzVxTlGNlrj9aAaA274U9JYmpQnaLsjii0Tid7ouFpkYGkTL7u9hMwqAwB++MRyj+TOSBW4oYE84SVuj/47hiFp/MR/URzFHSwpvRZ8NcdHWe+KycNUQn8hYRnk7OsP/CoKUGys5txnCU9cPISfrKWmtAOfRB4q//GJTxbb3DsNjx20WVGfUf8YqnfT7hszJR0NlL5zA==~3293747~4473155; _gid=GA1.2.1924151018.1640513767; ak_bmsc=BD5D54AB78186A1DFEA979946205CCF2~000000000000000000000000000000~YAAQJCEPF1QpmfB9AQAAYIs99g5yy/WQntJ3kIVQFUdQLzLt2lUj5FPJb9Usblx9fZdgNmfwxVuWSagn7zn3vsHrvPMAGQe2xWRuzH1ugoAGR13rxyhAQPnaezHaMu+8yBU/Z/F/kQMCs04cfet4QBT8YqUTrychHadJDc6cf6CePSXZehc3ObDBxefbZZ9lBxe9ErNU61G80MuFjx6iTjmhFJ+NV2yivn/FnN3+m5jE+zqWcR7dLUpl6dWxO0z4zTDef1F//67nclkhyecABRvzg3lrBkEpr9RIY7rMcyFcfQE/ga6pFllWJ9hWdb9MBCyq4jBwdj1Suz19XS5Wfd6u1YcTLpyI5uGkqjUcVx/RCwhPdYWwPuDqnv/iWH8SRiK0bq8DNNJCpZP9nITJ8uE6uQ3ASK9er1R9WEdcCoORaLRBW4rkmCVKPiGZKjtRVKkwjaGFUOmlMUZaLXOstT/aqJAEjqsbA96zBejRjxlSKwHitHyH1nChjI6k; usrcity=Mumbai; inweb_city=Delhi; scity=Delhi; dealBackCity=Delhi; main_city=Delhi; search_area=110043; inweb_what=Painters; profbd=0; bdcheck=1; tab=toprs; bd_inputs=2|4|House%20Painters; view=lst_v; detailmodule=011PXX11.XX11.180424202216.U7L8; showrtp=2%232021-12-26; docidarray=%7B%22011PXX11.XX11.210905190005.J3T6%22%3A%222021-12-26%22%2C%22011PXX11.XX11.180424202216.U7L8%22%3A%222021-12-26%22%7D; _abck=A6A56EBC4BCC6A1F862C743A8500A281~0~YAAQJCEPF0YxmfB9AQAAWjY+9gd3l+7Bzn5OUzJLxYi3HX2DI0fhimH1jTamDnTvnDajS31St6JYhaJ1E3BIwejOASNmKJVFwh98npPs9DYy+zMBqQ6L948l/g6HG9dZojL4UDYZhAevYZ1XqyaGet5udR9OYNy51fiDeXM6a0BhGyK+2RXSas4NSH5HLz677eCeMr+PRV7PAPjkIuUAuvq596R3Oe8WhvkFUI+11nw2us2XwGANbETBAhnz3G79JTnLcPeIVJp7mW+mCefBMY328GfzrmvUpVNb6zw6eX6/M0KaBMxbXStNwo1WiBjczuPjDJld8c6fEbKUhP4dYx2tFGaov+K5u8u1A9RmX2Yw7pTLAJlhNZZUsQr6wbRgx59misCEaO23EHuXd8l8svtOVgk5baOzIYs=~-1~-1~-1; prevcatid=11017366; BDprofile=1; AKA_A2=A; jdccp=1; Continent=AS; ppc=; _gat=1; _gat_UA-1220997-15=1; pincode=110075; sarea=Dwarka; PHPSESSID=53v9hi1nqdvmvtbrh6d5666jd7; _gat_category=1; bm_sv=1329A9B5366072CCE6D0EE0CCBBB939B~XFZVd/jMgT7bFWUMFmQm+TRWlC1SWBLtsKYTYV2eA0jaKmKVMsLIrnAji/WH9H6EAFqYgj/KENzwQpjgVrQRH0gUoPYv1HQaTXcsXVhEwQxpzccyrA/gYa6Yu5aq4VaowajbiuB/jILO36dhdB8wGCB6/AxlNr11pyErLW74ETI=; RT="z=1&dm=justdial.com&si=8007e297-9433-4567-b025-8f25ca169d28&ss=kxn7qgdm&sl=2&tt=gc&rl=1&obo=1&ld=t33&r=54nmf53m&ul=t34"',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
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

    base_url = 'https://www.google.com'
    driver.get(base_url)

    driver.find_element(By.CSS_SELECTOR, 'input[name="q"]').send_keys(query)

    driver.find_element(By.CSS_SELECTOR, 'span.mugnXc.Q0cixc').click()

    # select all links through soup
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Fetching all links
    links = soup.select('a.tHmfQe')

    if len(links) < no_of_records:
        fetch_rec = len(links)
    else:
        fetch_rec = no_of_records

    for i in links[:fetch_rec]:
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


def for_just_dial(query, cat, no_of_records=10):
    global driver, session, header

    r = session.get('https://www.justdial.com/' + query, headers=header)
    print('r.status_code :', r.status_code)
    print('r.text :', r.text)
    store_details = r.html.find('div.store-details')
    print('store_details :', len(store_details))
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

    return data_list


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        try:
            query = request.query_params
            state = query['state']
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

