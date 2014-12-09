Title: "Goodbye TinyMCE, Hello Markdown"
Tags: Django Markdown

I've been a faithful [TinyMCE](http://www.tinymce.com/) user for years, but
my blogging needs are growing and changing, and TinyMCE just isn't a fit
anymore. My primary complaint has been with syntax highlighting. The best
solution I was able to find was a Javascript libarary called
[SyntaxHighlighter](http://alexgorbatchev.com/SyntaxHighlighter/) that
requires you to plug into the customization settings of TinyMCE and be
fastidious about embedding the right Javascript libraries and CSS stylesheets.
While it has served its purpose, I've determined that my setup was, among
other negatives, WYSIWYG first, everything else second.

Recently I discovered
[markdown](http://daringfireball.net/projects/markdown/). Yes, I'm a late
bloomer. It is everything I ever wanted and nothing I never needed. Also,
Django comes fully ready for markdown syntax. For highlighting I chose the
ever-popular [pygments](http://pygments.org/) library. Installing pygments
is as easy as a quick pip install. Markdown also had to be installed prior to
following a breezy [guide](https://docs.djangoproject.com/en/dev/ref/contrib/markup/#id1) on
the Django docs. I dug through multiple editors for the admin before finally
choosing [django-markitup](https://bitbucket.org/carljm/django-markitup/overview), a did-the-hard-part-for-you Django app that provides
model and form hooks for the awesome
[Markitup](http://markitup.jaysalvat.com/home/) Javascript editor. I
[forked](https://github.com/dustinfarris/django-markitup) it to make a
minor edit to the Javascript configuration (doesn't have tab-button logic out
of the box for some reason). After all is said and done, I am able to write
standard, syntax highlighted markdown in Django admin, as simple as:

{% raw %}
```django
{% load markup %}
{{ object.content|markdown:"codehilite"|safe }}
```
{% endraw %}

which results in:

{% raw %}
```django
{% load markup %}
{{ object.content|markdown:"codehilite"|safe }}
```
{% endraw %}

The markdown templatetag honors
HTML, so my existing blog entries don't even have to be modified! I'll
probably convert a few of them anyway.
