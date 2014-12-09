Title: "Cache Timeout Default in Django"
Tags: Django

I had to break a bad habit where I always specify explicit cache timeout settings when building custom template tags.  For example, I might have a news feed for the homepage that looks something like this:

```python
    from django.conf import settings
    from django.core.cache import cache
    from django.template import Library

    from news.models import Article


    register = Library()



    @register.inclusion_tag('news/_news-feed.html')
    def show_news_feed():
        """Display 3 most recent news articles."""
        latest_articles = cache.get('news_latest_articles')
        if not latest_articles:
            latest_articles = Article.objects.order_by('-pub_date')[:3]
            cache.set(
                'news_latest_articles',
                latest_articles,
                settings.NEWS_LATEST_ARTICLES_TIMEOUT)
        return {'latest_articles': latest_articles}
```

Notice that I use a custom value for the timeout duration, which means somewhere in my ``settings.py`` I have to have:

```python
    NEWS_LATEST_ARTICLES_TIMEOUT = 600
```

or something like that.  However, there is a default value already available when you set up your cache backend.  Usually this looks something like this in ``settings.py``:

```python
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': '',
            'TIMEOUT': 300,
            'VERSION': 1,
        }
    }
```

Note the timeout value here.  This value is used as a default whenever you import the ``cache`` module from ``django.core``.  In fact, 300 seconds is the default value [regardless][1], so you could even leave it out here.  Best to stay DRY unless otherwise needed.

[1]: https://docs.djangoproject.com/en/1.4/ref/settings/#timeout
