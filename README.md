# Csfd
Top 300 movies from csfd.cz with their actors in Django


## Installation

pip install -r requirements

## Usage

`python manage.py runserver` to start local server

## Testing

`python manage.py test csfd.tests`

## Database

Populated db.sqlite3 is already included in the project.
If you need to repopulate database, you can delete sqlite file and run `python scraper.py` in csfd subfolder.

There is also /perform-scrape page, but it's considerably slower for this task.
