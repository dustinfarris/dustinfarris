Title: "Offering an RSS Filter Option"
Tags: RSS

The great thing about RSS is that it allows you to get updates on things you're interested in as they are published.  However, with multifaceted blogs, such as mine, it's quite possible that you are receiving both wanted and unwanted updates from your subscription.  That's why I've decided to fork off part of my RSS feed to only propagate "technical" blog posts.

I modified my feed class so that it can generate complete or filtered feeds on demand:

```python
    class BlogFeed(Feed):
        title = "Dustin Farris"

        def __init__(self, techie_filter=False):
            self.techie_filter = techie_filter

        def items(self):
            qs = Entry.published.all()
            if self.techie_filter:
                qs = qs.filter(techie=True)
            return qs[:10]
```

This allows me to have an RSS page that offers the filtered option in urls.py:

```python
    # Blog feeds
    url(r'^feeds/$', direct_to_template, {'template': 'blog/feeds.html'}, name='feeds'),
    url(r'^feeds/all/$', BlogFeed(), name='feed-all'),
    url(r'^feeds/techie/$', BlogFeed(techie_filter=True), name='feed-techie'),
```

I think RSS should be all about beaming the right information to the right people.  Check out the new and improved [RSS page](http://dustinfarris.com/feeds/) for dustinfarris.com.
