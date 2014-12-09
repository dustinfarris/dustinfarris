Title: "Django, jQuery, and Infinite Scroll"
Tags: Django jQuery

**Incomplete**: This post is missing some JavaScript code that got removed
somehow when I [switched to Octopress](http://dustinfarris.com/2013/06/from-django-to-github-pages/).

As the "next page" button becomes a thing of the past, we look for new ways to
provide streaming information. Enter infinite scroll. Implementing infinite
scroll in Django is easy thanks to the built-in
[paginator](https://docs.djangoproject.com/en/dev/topics/pagination/). What
you need is a view that will generate additional results of an object when
called upon via AJAX. Assume this model in a "people" application:

```python
class Person(models.Model):
    name = models.CharField()
    age = models.IntegerField()
```

Build this view to generate the list page _and_ handle
AJAX calls for more results:

```python
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render
from people.models import Person

def people_list(request):
    # If this isn't AJAX, just return the page
    if not request.is_ajax():
        return render(request, 'people/people_list.html')
        people_qs = Person.objects.all().order_by('name')
        # Get the paginator
        paginator = Paginator(people, 5)
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            people = paginator.page(page)
        except (EmptyPage, InvalidPage):
            people = paginator.page(paginator.num_pages)
        # Return a snippet
        context = { 'people': people, 'paginator': paginator, }
        return render(request, 'people/_people_list.html', context)
```

The snippet is fairly simple.
_people_list.html:

{% raw %}
```django
{% for person in people %}
    <li{% if people.has_next %} data-next="{{ people.next_page_number }}"{% endif %}>
        Name: {{ person.name }}
        Age: {{ person.age }}
{% endfor %}
```
{% endraw %}

And in in the main page, we enable the whole thing with
JavaScript. people_list.html:

And there you have it. Alternate jQuery infinite scroll techniques can be
[found here](http://www.jquery4u.com/tutorials/jquery-infinite-scrolling-demos/).
