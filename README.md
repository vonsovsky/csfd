# Csfd
Top 300 movies from csfd.cz with their actors in Django


## Installation

pip install -r requirements

or

poetry install

## Usage

`python manage.py runserver` to start local server

## Testing

`python manage.py test`

## Re-populate lists in database

Populated db.sqlite3 is already included in the project.

If you need to repopulate database, you can delete db.sqlite3 file and start over again. Run
`python manage.py migrate` to create new data structure and `python scraper.py` to download and store data from csfd.cz.
