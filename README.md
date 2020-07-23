# Csfd
Top 300 movies from csfd.cz with their actors in Django


## Installation

pip install -r requirements

## Usage

`python manage.py runserver` to start local server

## Testing

`python manage.py test csfd.tests`

## Re-run list of movies

Populated db.sqlite3 is already included in the project.

If you need to repopulate database, you can delete sqlite file and run
`python manage.py migrate` to create new data structure to be re-filled by `python scraper.py`.
