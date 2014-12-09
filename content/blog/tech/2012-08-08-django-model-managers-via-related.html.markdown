Title: "Django Model Managers via Related"
Tags: Django

It is fairly common practice to use a custom model manager when you have a certain field(s) that you know you will be filtering by a lot.  I found a small caveat from the traditional approach when you take related objects into account.  Take this classic example for published blog posts:

```python
class Author(models.Model):
    name = models.CharField(max_length=40)

class PostManager(models.Manager):
    def published(self):
        return super(PostManager, self).get_query_set().filter(published=True)

class Post(models.Model):
    title = models.CharField(max_length=40)
    author = models.ForeignKey(Author, related_name='posts')
    content = models.TextField()
    published = models.BooleanField()

    objects = PostManager()
```

All is fine and dandy in a template if you ask for {% raw %}{{ post_list.published }}{% endraw %}, but a problem arises when you utilize the custom manager function through the related field; {{ "{{ author.posts.published "}}}} gives an iterator with _all_ posts, not just the ones related to the author!

I haven't had time to figure out the mechanics of this phenomena, but to get things working as expected we have to make use of the ``all()`` function of the superclass rather than ``get_query_set()``.  It seems the latter is unaware of any related instantiations.

```python
return super(PostManager, self).all().filter(published=True)
```

Another possible workaround would be to have to completely separate managers, one called published, and the other called objects, where the published manager overrides ``get_query_set`` instead of adding an additional method:

```python
class PublishedPostManager(models.Manager):
    def get_query_set(self):
        return super(PublishedPostManager, self).get_query_set().filter(is_published=True)

class Post(models.Model):
    ...
    is_published = models.BooleanField()

    published = PublishedPostManager()
    objects = models.Manager()
```
