import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import lxml_html_clean

header = {"uer-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

url = "https://www.op.gg/summoners/oce/Bagiorno-OCE?queue_type=SOLORANKED"





def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.prettify()

def get_win_rate(soup):
    stats = soup.find('div')
    # win_rate = stats.find('div', class_='win-lose')
    return stats

#print(get_win_rate(get_soup(url)))
# print((requests.get(url)).content)
# print(get_soup(url))


session = HTMLSession()
response = session.get(url)
print(response.status_code)