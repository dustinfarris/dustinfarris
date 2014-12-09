Title: "Django: A New Way to Write Tests"
Tags: Django RSpec

Taking a lot of inspiration from Ruby's [RSpec][1], I've established a new way to write my tests when doing TDD in Django.  Using [django-nose][2], [factoryboy][3], and a few of my own [helpers][4] I have greatly simplified and consolidated test writing.

My file structure:

```text
project
  |
  +-- app1
  |
  +-- app2
  |
  +-- project
  |
  +-- tests
        |
        +-- models
        |     |
        |     +-- app1_models.py
        |     |
        |     +-- app2_models.py
        |
        +-- requests
        |     |
        |     +-- app1_pages.py
        |     |
        |     +-- app2_pages.py
        |
        +-- views
        |     |
        |     +-- app1_views.py
        |     |
        |     +-- app2_views.py
        |
        +-- support
        |     |
        |     +-- utilities.py
        |
        +-- factories.py
```

For brevity I skipped over the ``__init__.py`` files.  You can see the tree in full [here][5].

The ``utilities.py`` file contains some helper code I've written that expands on the assertions provided by Nose and provides a few other shortcuts.  When all is said and done, we get three basic types of tests: models, requests, and views.

As an example for "app1" model tests, suppose app1 is a blog application:

```python
from tests.support.utilities import *
from tests.factories import *

class BlogModel(TestCase):

  def test_fields(self):
    it = get_model(BlogFactory())

    it.should_respond_to('pub_date')
    it.should_respond_to('last_modified')
    it.should_respond_to('title')
    it.should_respond_to('author')
    it.should_respond_to('content')
    it.should_respond_to('slug')
    it.should_be_valid

  def test_with_blank_title(self):
    it = get_model(BlogFactory.build(title=''))

    it.should_not_be_valid

  def test_with blank_content(self):
    it = get_model(BlogFactory.build(content=''))

    it.should_not_be_valid
```

And so on.  Here is an example of a "requests" test.

```python
from app1.models import Blog
from tests.factories import *
from tests.support.utilities import *

class BlogPages(TestCase):

  def test_index(self):
    for _ in range(3):
      BlogFactory()

    page = visit('blog:index')

    for e in Entry.objects.all()[:3]:
      page.should_have_html('<span>%s</span>' % e.title)

  def test_blog_page(self):
    blog = BlogFactory()

    page = visit(blog)

    page.should_have_html('<title>%s</title>' % blog.title)
    page.should_contain(blog.author.first_name)
```

And so on.  Finally, the "views" tests.  Suppose app2 is a contact form application:

```python
from app2.models import Message
from tests.support.utilities import *

class ContactViews(TestCase):

  def test_message_creation_with_invalid_information(self):
    old_message_count = Message.objects.count()
    ajax('post', 'contact', {})
    assert_equal(Message.objects.count(), old_message_count)

  def test_message_creation_with_valid_information(self):
    old_message_count = Message.objects.count()
    message = {
      'name': "Sample Person",
      'email': "person@email.org",
      'message': "This is an example message."}
    ajax('post', 'contact', message)
    assert_equal(Message.objects.count(), old_message_count + 1)
```

I think having tests arranged this way is much more comprehensive and readable. I've been "testing" the tests on this blog using [Travis][6] continuous integration and have been very pleased. Feel free to look at the [source][7] code for ideas.

[1]: http://rspec.info
[2]: https://github.com/jbalogh/django-nose
[3]: https://github.com/dnerdy/factory_boy
[4]: https://github.com/dustinfarris/dustinfarris/blob/master/tests/support/utilities.py
[5]: https://github.com/dustinfarris/dustinfarris/tree/master/tests
[6]: https://travis-ci.org
[7]: https://github.com/dustinfarris/dustinfarris
