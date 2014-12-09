Title: "Testing in Django"
Tags: Django
published: false

Writing tests and test-driven development has become all the rage lately; but before declaring assertions left and
right, it's important to consider where, why, and how you will write your tests.

Different frameworks have different philosophies about how to go about this but, more often than not, developers tend
to create their own style or use the style of third-party test libraries.  While there is nothing wrong with differing
styles, you should take care to ensure that your are being efficient and effective.

This is my (by no means authoritative) take on the three important divisions of testing (unit/integration/functional)
in Django.

Unit Tests
----------

The most basic level of testing is unit testing.  This is where you ensure your module uses other (already tested)
modules the way it should.  They are absolutely the least complex, no-brainer-type tests you will ever write.

Think about unit tests like hooking up cars on a train.  When you hook up a car on the end of a train you'll double-
check that it is indeed fastened to the car in front of it.  You won't recheck the entire train because you assume
whoever hooked up the cars in front did their part ensuring everything was in place.

For example, say I have a filter I call often so I put it into a module:

``` python
def get_authors(library):
    return Author.objects.filter(books__library=library)
```

We know that Django's ORM works—it is _very_ well tested—so there is no need to re-test it.  What we do need to
test, though, is that our function utilizes the ORM the way we want.  We accomplish this with a unit test and a
wonderful library called [Mock](http://www.voidspace.org.uk/python/mock/). (now
[included](http://docs.python.org/3/library/unittest.mock.html) in Python 3.3 and up)

Installing Mock is easy with pip: ``pip install mock``

Mock replaces a module with a fake module that intercepts calls and records them along with any arguments involved.
Using mock in our example, we can show that our method calls ``Author.objects.filter`` without actually running it.

The basic usage of Mock is first setting it up:

```python
my_mock = Mock(return_value="something")
```

And then asserting that it was called with any number of arguments:

```python
my_mock.assert_called_with(myarg=myvalue)
```

For our Django unit tests, we'll use Mock's ``patch`` decorator which declares a Mock for the duration of the test:

```python
@patch('mymodule.mymethod')
def test_something(self, mymethod_mock):
    do_something()
    mymethod_mock.assert_called_with()
```

Here's what a unit test looks like for our example:

```python
import unittest

import mock

from myapp.mymodule import get_authors


class GetAuthorsTest(unittest.TestCase):

    @mock.patch('myapp.mymodule.Author')
    def test_get_authors(self, AuthorMock):
        Author.objects.filter = mock.Mock(return_value="ReturnMock")

        result = get_authors("library_mock")

        Author.objects.filter.assert_called_with(books__library="library_mock")
        self.assertEqual("ReturnMock", result)
```

In summary, we:

* "Patched" our test by mocking Author.  Note that we reference Author as and object
    within our module, not from it's original source which probably would have been
    something like ``myapp.models.Author``.  Also note that mock patches are passed to
    your function as arguments which can be any name you like.  I chose ``AuthorMock``.

* Piggybacked another mock, ``objects.filter``, on top of the AuthorMock.  You'll
    find that mocks are very flexible once they've been created.

* Assigned a return value to the objects.filter mock.  We test for this later.

* Called the function we want to test with a dummy argument.

* Asserted that our mock was indeed called with the appropriate arguments.

* Asserted that the function did indeed return the result of that call, which in
    this case should be the value we gave to return_value.

We accomplished all this without actually touching the Django ORM, but now we know for sure that when mocks are put
aside, this function will operate correctly.

Why do we do it this way?  Why not create some dummy data in the database in and see if it produces the right results.
Well we actually will do that later, in the form of integration tests.  Unit tests have two big benefits:

* They reduce false-positives by ensuring your code is utilizing the right code
    rather than producing the right results (which could be right for your test, but
    wrong in other scenarios)

* They are very, _very_ fast.

Notice we don't even use Django's ``TestCase``.  We don't need it.  For some unit tests you may, but often Python's
``unittest`` library and mock are all you need.  These tests will run insanely fast, and for that fact, you can get
into the habit of running them periodically while you're developing.

As you build your application, each building block should be unit tested.  This will increase confidence in your
architecture especially when you add features to existing code.


Integration Tests
-----------------

These are usually the most common tests that beginners right because they tend to be pretty straight-forward, and don't
require much thought.  Integration tests essentially are meant to accomplish "if I put in input A, do I get expected
output B?"

In Django, integration tests ensure that your modules and views are generating the content you expect them to.

The easiest way to write integration tests in Django is to use the ``TestClient`` that Django provides which allows you
to fake browser requests and see what sort of responses you get back from you application.

Say we have this very basic view:

```python
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    context = {'blog': blog}
    return render(request, "blog/blog_detail.html", context)
{% endhighlight %

There are really two scenarios we would want to test for here:

1. Scenario in which the blog exists
2. Scenario in which the blog does not exist

In scenario 1 we would expect the view to return a success (200) response after rendering the blog_detail template.  In
scenario 2 we would expect the view to return a not-found response (404).

To accomplish this we will use another common testing apparatus called a fixture.  The Mock library provides a
decorator to make this easy.  Essentially, you write an instance method in your test case that defines the fixture.
For example:

```python
@fixture
def user(self):
    return User.objects.create(username="bob")
```

Here is how we would write a test using Django's TestClient:

```python
import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from myblogapp.models import Blog
from myblogapp.views import blog_detail


class BlogDetailTest(TestCase):

    @mock.fixture
    def blog(self):
        return Blog.objects.create(
            title="BlogMock", content="BlogMock")

    def test_when_blog_exists(self):
```

