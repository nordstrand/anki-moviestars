import os
import genanki
from pathlib import Path

from wikipedia import *

def main():
    movies = get_movies()[:5]
    print(f"Movies: {len(movies)}")
    actors = [get_stars_from_movie(m['url']) for m in movies]
    flat_actors = [item for sublist in actors for item in sublist]
    print(f"Actors: {len(flat_actors)}")
    deduped_actors = list(set([hashabledict(f) for f in flat_actors]))
    print(f"Unique actors: {len(deduped_actors)}")
    actors_with_image_urls = [{"actor": a['actor'], "url": get_image_url_from_actor(a['url'])} for a in deduped_actors]
    for actor in actors_with_image_urls:
        if (actor['url']):
            download_image_for_actor(actor)
        else:
            print(f"Skipping image for {actor['actor']}")
    
    create_deck(actors_with_image_urls)


DATA_PATH="./images"
ANKI_PACKAGE_PATH="moviestars.apkg"

model = genanki.Model(
  1362513531,
  'Movie star Model',
  fields=[
    {'name': 'Name'},
    {'name': 'Picture'},
  ],
  templates=[
    {
      'name': 'Movie-kort',
      'qfmt': 'Name <br>{{Picture}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Name}}',
    }
  ])

def create_deck(actors):
    deck = genanki.Deck(2763120111, 'Movie stars')

    for actor in actors:
        deck.add_note(genanki.Note(
            model=model, 
            fields=[actor['actor'], f"<img src='{actor['actor']}.jpg'/>" ]))
    
    package = genanki.Package(deck)
    package.media_files = list(map(str, Path(DATA_PATH).rglob('**/*.jpg')))
    print(package.media_files)
    package.write_to_file(ANKI_PACKAGE_PATH)
    print(f"Anki output file {ANKI_PACKAGE_PATH} written.")

main()