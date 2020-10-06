import requests
import urllib3
from pyquery import PyQuery as pq
import pandas as pd

def parse_html(url):
    """
    解析html
    :param url: 爬取路由
    :return:
    """
    html = get_html(url)
    house_list = html('.LOGCLICKDATA').children('.info').items()
    result = []
    for house in house_list:
        house_message = parse_house(house)
        result.append(house_message)
    return result

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    urllib3.disable_warnings()
    request = requests.get(url, headers, verify=False)
    return pq(request.text)

def parse_house(house):
    title = house.children('.title').text()
    flood = house.children('.flood').text()
    address = house.children('.address').text()
    follow = house.children('.followInfo').text()
    tag = house.children('.tag').text()
    price = house.children('.priceInfo').text()
    message = dict(title=title,flood=flood,address=address,follow=follow,tag=tag,price=price)
    return message


if __name__ == '__main__':
    res = []
    for i in range(10):
        url = 'https://bj.lianjia.com/ershoufang/pg{}/'.format(i)
        house = parse_html(url)
        res = res+house
    df = pd.DataFrame(res)
    df.to_csv('../result/test.csv')


