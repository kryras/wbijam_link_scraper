import requests
from bs4 import BeautifulSoup

URL = 'https://enen.wbijam.pl/druga_seria.html'
baseURL = URL.split('wbijam.pl/', 1)[0] + 'wbijam.pl/'
player = 'mega' # mega vk sibnet cda vidlox mp4up 
page = requests.get(URL)
filename = "test.txt"


def get_episode_page_url(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for link in soup.find_all('table', class_='lista'):
        for a in link.find_all('a', href=True):
            links.append(baseURL + a['href'])
    links.reverse()
    return links


def get_player_page_url(links, player_name):
    urls = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        players = soup.find('table', class_='lista')
        player = players.find('td', text=player_name).find_parent('tr')
        playerURL = baseURL + 'odtwarzacz-' + \
            player.find('span', class_='odtwarzacz_link')['rel'] + '.html'
        urls.append(playerURL)
    return urls


def get_player_url(links):
    urls = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        urls.append(soup.find('iframe')['src'])
    return urls


def save_file(filename, links):
    with open(filename, 'w') as file:
        file.write('\n'.join(links))


episode_page_urls = get_episode_page_url(page)
player_page_urls = get_player_page_url(episode_page_urls, player)
players = get_player_url(player_page_urls)
save_file(filename, players)
