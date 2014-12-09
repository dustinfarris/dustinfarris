Title: "Facebook Meta-tags using Django and Jade"
Tags: Django

I've found the Facebook doesn't do the best job of inferring general information from my blog articles on its own.  Fortunately, the folks at FB provide a name-spaced meta tag schema more commonly known as [Open Graph][1].

Implementing a quick self-explanatory in a Django template [using Jade][2] is easy.  First we add a few extra items to our context before rendering:

```python
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404, render

from models import Entry


def entry_detail(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    context = {
        'entry': entry,
        'site': Site.objects.get_current(),
        'protocol': request.is_secure() and 'https' or 'http',
        'fb_image': getattr(settings, 'STATIC_URL') + 'img/logo.png',
    }
    return render(request, 'blog/entry_detail.jade', context)
```

And in the Jade template we can easily implement the Open Graph specifications.

```jade
block meta
    - with entry.content|markdown|striptags|truncatewords:23 as description
        meta(property='og:description', content='#{description}')
    meta(property='og:title', content='#{entry.title}')
    meta(property='og:image', content='#{protocol}://#{site}#{fb_image}')
    meta(property='og:type', content='article')
    meta(property='og:url', content='#{protocol}://#{site}#{entry.get_absolute_url()}')
    meta(property='og:site_name', content='Dustin Farris')
```

Now every time I write an article--which gets automatically posted to Twitter which is, in turn, synced with my Facebook timeline--I don't have to spend time deleting/revising the Facebook post.

[1]: https://developers.facebook.com/docs/opengraph/
[2]: http://dustinfarris.com/2012/6/django-and-jade/
