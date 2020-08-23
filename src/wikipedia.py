import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def get_movies():
    movies_url= "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    f = urllib.request.urlopen(movies_url)
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'html.parser')
    ths = soup.find("caption").parent.find_all("th")
    movie_ths=ths[6:]
    return [{"movie": m.find("a").text, "url": f"https://en.wikipedia.org/{m.find('a')['href']}"} for m in movie_ths]

def get_image_url_from_actor(actor_url):
    print(actor_url)
    f = urllib.request.urlopen(actor_url)
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'html.parser')
    infobox = soup.find("table", {"class": "infobox"})

    if infobox is None:
        return None

    img = infobox.find("img")
    if (img):
        return img["src"].replace("//", "https://")
    else:
        return None


def get_stars_from_movie(movie_url):
    f = urllib.request.urlopen(movie_url)
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'html.parser')
    infobox = soup.find("table", {"class": "infobox"})
    actors = infobox.find(text='Starring').parent.next_sibling.find_all('a')
    return [{'actor': a.text, 'url': f"https://en.wikipedia.org/{a['href']}"} for a in actors]

def get_best_actors():
    f = urllib.request.urlopen("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor")
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'html.parser')
    a = soup.find('table', {'class': 'sortable'}).find_all("img")
    return [{'actor': img.parent.find('a').text,
             'url':   f"https://en.wikipedia.org/{img.parent.find('a')['href']}"}
             for img in a][-30:]

def get_best_actresses():
    f = urllib.request.urlopen("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress")
    s = f.read().decode('utf-8')
    soup = BeautifulSoup(s, 'html.parser')
    a = soup.find('table', {'class': 'sortable'}).find_all("img")
    return [{'actor': img.parent.find('a').text,
             'url':   f"https://en.wikipedia.org/{img.parent.find('a')['href']}"}
             for img in a][-30:]

