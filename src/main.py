import os
import genanki
from pathlib import Path

from wikipedia import *

MIN_MOVIE_APPEARANCE=3

def main():
    movies = get_movies()
    print(f"Movies: {len(movies)}")
    actors = [get_stars_from_movie(m['url']) for m in movies]
    flat_actors = [item for sublist in actors for item in sublist]
    print(f"Actors in movies: {len(flat_actors)}")
    actor_appearances = {actor:flat_actors.count(actor) for actor in [hashabledict(a) for a in flat_actors]}
    filtered_actors = [actor for (actor,appearances) in actor_appearances.items() if appearances >= MIN_MOVIE_APPEARANCE]
    print(f"Unique actors with {MIN_MOVIE_APPEARANCE} or more movie appearances: {len(filtered_actors)}")
    actors_with_image_urls = [{"actor": a['actor'], "url": get_image_url_from_actor(a['url'])} for a in filtered_actors]
    for actor in actors_with_image_urls:
        if (actor['url']):
            download_image_for_actor(actor)
        else:
            print(f"Skipping image for {actor['actor']}")
    
    create_deck(actors_with_image_urls)


IMAGE_PATH="./images"
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
    package.media_files = list(map(str, Path(IMAGE_PATH).rglob('**/*.jpg')))
    print(package.media_files)
    package.write_to_file(ANKI_PACKAGE_PATH)
    print(f"Anki output file {ANKI_PACKAGE_PATH} written.")

main()