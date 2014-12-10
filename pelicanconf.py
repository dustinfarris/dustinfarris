#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Dustin Farris'
SITENAME = 'Dustin Farris'
SITEURL = 'http://localhost:8000'

THEME = 'pure-single'
COVER_IMG_URL = SITEURL + '/images/beach.jpg'
PROFILE_IMG_URL = SITEURL + '/images/dustin.jpeg'
LOGO_IMG_URL = SITEURL + '/images/df.png'
TAGLINE = 'inveniam viam aut faciam'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

DEFAULT_DATE = 'fs'

ARTICLE_PATHS = ['blog']
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
  ('github', 'https://github.com/dustinfarris/'),
  ('twitter', 'https://twitter.com/dustinfarris'),
  ('rss', '/feeds/all.atom.xml'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = [
  'images',
  'extra/CNAME',
  'extra/humans.txt',
  'extra/robots.txt',
  'extra/favicon.ico',
]
EXTRA_PATH_METADATA = {
  'extra/CNAME': {'path': 'CNAME'},
  'extra/humans.txt': {'path': 'humans.txt'},
  'extra/robots.txt': {'path': 'robots.txt'},
  'extra/favicon.ico': {'path': 'favicon.ico'},
}
