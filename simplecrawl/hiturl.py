from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("https://unsplash.com")
soup = BeautifulSoup(html.read(), 'html.parser')
for link in soup.find_all('img'):
    print(link.get('src'))
# print(html.read())
