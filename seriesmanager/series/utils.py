from .models import *

enter_menu = [{"title" : "Sign in", "url" : "login"},
        {"title" : "Sign up", "url" : "registration"},
        {"title" : "Home", "url" : "home"}]

exit_menu = [{"title" : "Logout", "url" : "logout"},
             {"title" : "Home", "url" : "home"}]


class Mixin:
    def get_context_mixin(self, request=None, **kwargs):
        context = kwargs
        if request and request.user.is_authenticated:
            context["menu"] = exit_menu
        else:
            context["menu"] = enter_menu
        return context


from urllib.parse import urlencode
import requests
import lxml.html as html

class SeriesSpiderItem:
    result = str()
    name = str()
    rating = str()
    years = str()
    countries = []
    genres = []
    description = str()



API = '95134f460dac16877f0a55bcda17fc62'


def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def get_info(category, dom, series):
    try:
        name = dom.xpath('//span[@data-tid="2da92aed"]/text()')[0]
    except IndexError:
        return
    description = dom.xpath('//p[@class="styles_paragraph__wEGPz"]/text()')[0].replace('\xa0', ' ')
    years = dom.xpath('//a[contains(@class, "styles_years")]/text()')[0]
    genres = dom.xpath('//a[contains(@href, "/lists/movies/genre")]/text()')
    countries = dom.xpath('//a[contains(@href, "/lists/movies/country")]/text()')
    rating = dom.xpath('//span[contains(@class, "styles_rating")]/text()')[0]
    if str(category).lower().replace('«', '').replace('»', '').replace('"', '') == \
        name.lower().replace('«', '').replace('»', '').replace('"', ''):
        series.result = 'Найден сериал:'
    else:
        series.result = 'Возможно, Вы имели в виду:'
    series.name = name
    series.description = description
    series.years = years
    series.genres = ', '.join(genres).strip()
    series.countries = ', '.join(countries).strip()
    series.rating = ''.join(rating).strip()
    return series


def parse(category):
    query = "https://www.kinopoisk.ru/index.php?kp_query=" + str(category).lower().replace(' ', '+')
    r = requests.get(get_url(query))
    page = r.content.decode('utf-8')
    response = html.document_fromstring(page)
    series = SeriesSpiderItem()
    series_name = response.xpath('//title[@data-tid="57f72b5"]/text()')
    if len(series_name) > 0:
        return get_info(category, dom=response, series=series)
    if len(series_name) == 0:
        series_id = response.xpath('//a[@data-type="series" and contains(@data-url, "/film/")]/@data-id')[0]
        cur_link = f"https://www.kinopoisk.ru/series/{series_id}/"
        cur_r = requests.get(get_url(cur_link))
        cur_page = cur_r.content.decode('utf-8')
        cur_response = html.document_fromstring(cur_page)
        return get_info(category, dom=cur_response, series=series)







