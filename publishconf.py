#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://dustinfarris.com'
COVER_IMG_URL = SITEURL + '/images/beach.jpg'
PROFILE_IMG_URL = SITEURL + '/images/dustin.png'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "dustinfarris"
GOOGLE_ANALYTICS = "UA-13275015-1"
