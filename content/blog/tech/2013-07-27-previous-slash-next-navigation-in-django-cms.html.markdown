Title: Previous/Next Navigation in Django CMS
Tags: Django

I don't know why Django CMS doesn't have a built-in helper for navigating a page tree.  Maybe this will be included in the upcoming [3.0 release][] (which I am very much looking forward to).

For now, here's a quick gist that will give you previous/next buttons to get from one page to the next in your CMS Page tree.

```django
{% load cms_tags %}
 
<ul class="pager">
  {% if current_page.get_previous_sibling %}
    <li><a href="{% page_url current_page.get_previous_sibling %}" role="prev">&larr; Previous</a></li>
  {% else %}
    <li><a href="{% page_url current_page.parent %}" role="prev">&larr; Previous</a></li>
  {% endif %}
  {% if current_page.children.exists %}
    <li><a href="{% page_url current_page.children.all|first %}" role="next">Next &rarr;</a></li>
  {% elif current_page.get_next_sibling %}
    <li><a href="{% page_url current_page.get_next_sibling %}" role="next">Next &rarr;</a></li>
  {% elif current_page.parent.get_next_sibling %}
    <li><a href="{% page_url current_page.parent.get_next_sibling %}" role="next">Next &rarr;</a></li>
  {% elif current_page.parent.parent.get_next_sibling %}
    <li><a href="{% page_url current_page.parent.parent.get_next_sibling %}" role="next">Next &rarr;</a></li>
  {% endif %}
</ul>
```


[3.0 release]: https://www.django-cms.org/en/blog/2013/07/03/django-cms-3-beta-2/
