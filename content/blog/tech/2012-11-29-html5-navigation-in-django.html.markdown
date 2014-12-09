Title: "HTML5 Navigation in Django"
Tags: Django HTML5

Creating a snappy user experience can be easily obtained by implementing [HTML5 navigation](http://dev.w3.org/html5/spec/history.html#history).  Not only does it take less time to render only the needed Django templates, the browser has less information to digest on the response.

Note that I do not use the popular method of using jQuery to request a page, then parsing out the elements I want to replace.  No, this method intelligently renders only the appropriate "snippet" templates and returns the HTML in a JSON response.

I'll use [CoffeeScript](http://coffeescript.org/), [Jade](http://jade-lang.com/), and of course Python in this example.  Don't worry if you're not familiar with the first two as it is fairly easy to understand what is going on and convert to the JavaScript and HTML equivalents.

<a id="contents"> </a>
## Contents

* [Planning](#planning)
* [Templates](#templates)
* [Response Objects](#response-objects)
* [Views](#views)
* [Scripting it together](#scripting-it-together)
* [Conclusion](#conclusion)

<a id="planning"> </a>
## Planning

Before we can start building the navigation script, we need to decide which parts of the page we want to (re)load.  Take a basic (common) example:

![Normal web page layout](/media/filer_public/2012/11/29/normallayout.png)

Say the content area is what we'll be after most of the time, but sometimes maybe the sidebar changes to.  Perhaps it holds user information that would change when a user logs in or edits their profile.  To be on the safe side, we will want to refresh the ``#main > article`` and ``#main > aside`` containers on every navigation event.  Moving on.

<a id="templates"> </a>
## Templates

This is where we make decisions based on our "planning."  Based on our layout, we'll use a base template that looks something like this in ``myproject/templates/base.jade`` (in Jade):

```jade
!!! 5

html
    head
    title
        block title
        | My Project
    body
    header
        block header
        include _header
    #main
        aside
        include _aside
        article
        block content
    footer
        block footer
        include _footer
```

I'm leaving out the other usual stuff (jQuery, stylesheets, etc..) for brevity.  The two areas we are concerned with, again, are the 'aside' and 'article' areas under ``#main``.  The aside area will probably be built with one template, in our case, ``myproject/templates/_aside.jade``:

```jade
if request.user.is_authenticated
    p Welcome back!
else
    p You are not registered
```

Or something like that.  The content area is more interesting.  For every "view" we will need a full template and template snippet.  The template snippet is used for HTML5 AJAX requests, the full template for regular requests.

Suppose we have a blog app/model.  Using a blog 'detail' view as an example, we will have two templates.  The first, ``myproject/blog/templates/blog/detail.jade``:

```jade
extends base

block title
    | {{ object.title }}

block content
    include blog/_detail
```

That's it, just a skeleton, and the meat goes in the snippet, ``myproject/blog/templates/blog/_detail.jade``:

{% raw %}
```jade
header
  h1 {{ object.title }}
    p Written by {{ object.author }}

{{ object.content|safe }}
```
{% endraw %}

[Table of Contents](#contents)

<a id="response-objects"> </a>
## Response Objects

A big part of the HTML5 navigation process is the HTTP response. As I mentioned, we will be compiling the HTML into a JSON response, and I've found it saves a lot of time to put a couple wrappers on Django's standard HttpResponse class.  (At the risk of confusion, I'm also going to throw in a 'redirect' class which will come in very handy for many people).  I like to put this in an 'http' module under my project module.  ``myproject/http.py``:

```python
import json

from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode


class JsonResponse(HttpResponse):
    def __init__(self, request=None, title='', article_template='', context={},
        aside_template='_aside.jade'):
    request_context = RequestContext(request, context)
    content = json.dumps({
        'title': render_to_string(article_template, request_context),
        'article': render_to_string(aside_template, request_context)})
    super(JsonResponse, self).__init__(
        smart_unicode(content), content_type='application/json')


class JsonRedirect(HttpResponse):
    def __init__(self, url):
    content = json.dumps({
        'redirect': url})
    super(JsonRedirect, self).__init__(
        smart_unicode(content), content_type='application/json')
```

The JsonResponse object will give us a JSON response containing the new pages title, sidebar content, and main content.  We'll use this later.

[Table of Contents](#contents)

<a id="views"> </a>
## Views

Now it's up to the view to return the appropriate response.  This part is really quite straight forward.  For our example detail view, we'll just make a minor adjustment to the Django's detail generic view. ``myproject/blog/views.py``:

```python
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.generic.detail import DetailView
from myproject.http import JsonResponse


class BlogDetailView(DetailView):

    @method_decorator(vary_on_headers('X-Requested-With'))
    def dispatch(self, *args, **kwargs):
    return super(BlogDetailView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **kwargs):
    if self.request.is_ajax():
        return JsonResponse(
        self.request, self.object.title, 'blog/_detail.jade', context)
    return render(self.request, 'blog/detail.jade', context)
```

To quickly summarize, we are determining how the page is being requested, by AJAX(HTML5), or as a normal request(not HTML5), and returning the snippet, or the full page respectively.

We do a minor override on the ``dispatch`` method to make sure caching doesn't confuse our logic---for example if the page is requested as AJAX and Django caches the response, then the page is requested normally and Django returns the same JSON object.  The ``vary_on_headers`` decorator effectively gives us two cache slots for the view.

[Table of Contents](#contents)

<a id="scripting-it-together"> </a>
## Scripting it together

Now we take our server logic and implement it client-side.  We want to capture all 'a' clicks and run it through HTML5.  I'm including all the necessary code to make this work, which should mostly make sense if you are already familiar with how HTML5 pushState works.  (I use [Modernizr](http://modernizr.com/) for feature detection) I'm also including a couple extra goodies like redirect handling and Google Analytics logic.  ``myproject/static/javascripts/main.coffee``:

```coffee-script
# Navigation handling

if Modernizr.history
    # Initialize history state
    history.replaceState
    title: document.title
    article: $('#main > article').html()
    aside: $('#main > aside').html()
    , document.title, window.location

    # Navigate to a new page
    goTo = (url) ->
    # First, set a query-string to prevent browsers from caching
    # the JSON response.  (a known issue in Chrome)
    if url.indexOf("?") is -1
        get_url = url + '?dontcacheme=1'
    else
        get_url = url + '&dontcacheme=1'

    # Send the request and handle the response
    $.get get_url, (response) ->
        # Are we being redirected?
        if response.redirect isnt undefined
        return goTo response.redirect
        # Nope, continue on
        history.pushState
        title: response.title
        article: response.article
        aside: response.aside
        , response.title, url
        document.title = response.title
        $('#main > article').html response.article
        $('#main > aside').html response.aside
        captureNavigation #main

        # Alert Google Analytics
        if typeof window._gaq isnt 'undefined'
        window._gaq.push ['_trackPageView', url]

        # Make sure we start at the top
        $(document).scrollTop 0

    # Capture "a" click events.. let's do this
    captureNavigation = (parent) ->
    $("#{parent} a:not(no-html5)").on 'click', ->
        if $(this).attr('rel') is 'external' or $(this).attr('target') is '_blank'
        return true
        goTo($(this).attr('href'))
        return false

    # "$(document).ready" for non-coffeescript users ;)
    $ ->
    captureNavigation 'body'
```

There are few things to clarify here.  First is the ``dontcache=1`` query-string.  This is solely to address a bug in Chrome where it will otherwise cache responses and reuse them inappropriately for future requests.

Also, it is important that the ``captureNavigation`` function focuses only on areas that are new to the window; otherwise you end up with a stack of event handlers on some of your elements.  Tune as desired.

[Table of Contents](#contents)

<a id="conclusion"> </a>
## Conclusion

This gives you a slick HTML5 navigable site, and the performance bump is immediately noticeable.  It is amazing how much faster browsers parse JSON responses over HTML.

There is more to consider here.  Handling forms have a couple quirks, and there's plenty of room for creativity in terms of layouts and packing extra information into the JSON responses.  Let me know in the comments if you need help with any of these.
