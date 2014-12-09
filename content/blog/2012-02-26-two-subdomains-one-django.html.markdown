Title: "Two Subdomains, One Django"
Tags: Django

I want to serve two sub-domains from the same Django project--not unheard of,
see the countless multi-lingual sites out there. My goal,
however, is specifically to share the whole project, except for the URLs.
In theory, I could make use of
Django's["sites" framework](https://docs.djangoproject.com/en/dev/ref/contrib/sites/). The first thing to do is create
two "sites" in the back-end, then identify a specific one in two different
settings files.

One for subdomain abc:

```python
# settings_abc.py
from settings_base import *

SITE_ID = 1
```

And another for subdomain xyz:

```python
# settings_xyz.py
from settings_base import *

SITE_ID = 2
```

Then in `urls.py`, I could create a conditional statement like so:

```python
# urls.py
from django.conf import settings
from django.contrib.sites.models import Site
...

curent_site = Site.objects.get(id=settings.SITE_ID)
if current_site.domain == 'abc.domain.com':
    urlpatterns = ( ... )
elif current_site.domain == 'xyz.domain.com':
    urlpatterns = ( ... )
```

This is me thinking out loud. I'll have to test it live to
see how well it works. Eventually, I'd like one general
purpose sub-domain, and then another sub-domain to serve secure content.

  *[URL]: Universal Resource Locator
