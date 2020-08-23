from __future__ import print_function
import requests
from wand.image import Image
from wand.drawing import Drawing
from wand.font import Font
from wand.color import Color
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup

#url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Robert_Downey_Jr_2014_Comic_Con_%28cropped%29.jpg/220px-Robert_Downey_Jr_2014_Comic_Con_%28cropped%29.jpg'
#url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Julia_Roberts_%2843838880775%29.jpg/440px-Julia_Roberts_%2843838880775%29.jpg'

def save_image_with_attribution(actor):
    resp = requests.get(actor['url'])
    try:
        with Drawing() as draw:
            with Image(blob=resp.content) as img:
                print('format =', img.format)
                print('size =', img.size)
                attribution = get_attribution_if_attribution_is_required(actor['url'])

                if attribution:
                    img.caption(f"By {attribution}",
                    font=Font("SourceSansPro-Regular.otf", max(12, 0.02*img.size[1]) , Color("#fff")),
                    gravity="south")

                img.save(filename=f"images/{actor['actor']}.jpg")
    finally:
        resp.close()


def get_attribution_if_attribution_is_required(url):
    image_title=re.match(r'.*/(?:[0-9]*px-)?([^/]*)$', urlparse(url).path)[1]
    print(image_title)

    requesturl=f"https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&format=json&titles=File:{image_title}"
    print(requesturl)
    resp = requests.get(requesturl)
    print(resp.json())
    attributionRequired = resp.json()['query']['pages']['-1']['imageinfo'][0]['extmetadata']['AttributionRequired']['value'] == 'true'
    print(attributionRequired)
    if attributionRequired:
        artist=resp.json()['query']['pages']['-1']['imageinfo'][0]['extmetadata']['Artist']['value']
        artistText=BeautifulSoup(artist, 'html.parser').text
        return artistText
    else:
        return None