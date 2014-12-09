Title: "Linking Multiple RSS Feeds"
Tags: RSS

I [split my RSS feed](http://dustinfarris.com/2012/5/offering-rss-filter-option/) the other day to filter technical blog posts from the rest by creating a /feeds/ page that offers the option.  Little did I know that these options can be presented right in the head of an HTML document just by adding additional "links"

{% raw %}
```django
    <link
        rel="alternate"
        type="application/rss+xml"
        title="RSS 2.0 - All blog entries"
        href="{% url blog:feed-all %}">
    <link
        rel="alternate"
        type="application/rss+xml"
        title="RSS 2.0 - Technical entries only"
        href="{% url blog:feed-techie %}">
```
{% endraw %}

Done.

![Multiple RSS in Chrome](/media/filer/2012/05/28/multiple-rss.png)
