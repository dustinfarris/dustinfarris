Title: "Django and Jade"
Tags: Django

This week I made an important addition to my tool kit.  In the past I've focused primarily on ways to streamline backend development using tools like django_compressor, Sentry, and Fabric.  More recently, however, I've taken a turn and began focusing on ways to bring my frontend up to speed.

My initial focus was on incorporating new tools and resources like SASS, HTML5, Markdown and microdata (blog posts to follow).  I'd like to focus here, though, on my latest addition, Jade.

[Jade][1] is a HTML preprocessor that dramatically reduces the bloat and messiness of your code.  It uses indented syntax(hey, kind of like Python!) and is extremely easy to learn.  Also, thanks to some terrific work by [Syrus Akbary][2] who ported Jade to Python, it integrates easily with Django.

To get the full experience you will need PyJade by Syrus, and the Python Markdown library (if you plan to use Markdown, which I highly recommend).  Both are available on PyPi.

    pip install Markdown
    pip install pyjade

Install pygments also if you plan on publishing code--see my post on [syntax highlighting][3] with Markdown.

Enabling Jade couldn't be easier.  PyJade comes with a Django "extension" which features a template loader.  The loader wraps your existing loaders.  This allows PyJade to do the Jade preprocessing first, before handing the template off to the usual suspects.  All it takes a simple modification to your settings.py ``TEMPLATE_LOADERS`` variable.

```python
    TEMPLATE_LOADERS = (
        ('pyjade.ext.django.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )),
    )
```

With the loader in place, any '.jade' template you use in Django will be intercepted by PyJade and preprocessed.  Here is an example "base.jade":

{% raw %}
```jade
    !!! 5
    html
        head
            title
                block title
                    | My Website
        body
            header
                h1 My Website
                nav
                    a(href!='{% url home %}') Home
                    a(href!='{% url blog:index %}') Blog
                    a(href!='{% url about %}') About Me
            #main(role='main')
                block content
                    p Welcome to my website
            footer
                p All content copyright by me.
```
{% endraw %}

Then I can do an about page.  First, in urls.py:

```python
    from django.views.generic.simple import direct_to_template

    urlpatterns = patterns('',
        url(
            r'^about/$',
            direct_to_template,
            {'template': 'about.jade'},
            name='about'
        ),
        ...
```

And create about.jade which might look something like this:

```jade
    extends base

    block title
        | About Me

    block content
        article
            header
                h1 About Me
            :markdown
                This is a page about me.  Be sure to check
                out my [Facebook Profile][1] where I post lots
                of crazy pictures!

                [1]: http://facebook.com/dustinfarris
```

Because Jade is so easy to learn and use, the time investment really pays off.  I personally love how it feels sort of Pythonic with regards to indented syntax, and kicking out templates has certainly received a speed boost!

[1]: http://jade-lang.com/
[2]: https://github.com/SyrusAkbary/pyjade
[3]: http://dustinfarris.com/2012/5/goodbye-tinymce/
