Title: "&quot;subject&quot; Decorator for Django Tests"
Tags: Django Python

The Python elite will probably turn their noses up at me, but I just conjured an _even_ better looking way to write my [tests][1].

Using my [utilities.py][2] file I can write the following decorator:

```python
def subject(item):
  def wrapper(f, _item=item):
    def test_func(*args, **kwargs):
      item = _item
      if models.Model in item.__class__.__bases__:
        item = get_model(item)
      f.__globals__['it'] = item
      res = f(*args, **kwargs)
      return res
    return test_func
  return wrapper
```

which allows me to write tests that look like this:

```python
@subject(BlogFactory.build(title=''))
def test_with_blank_title(self):
  it.should_not_be_valid
```

[1]: http://dustinfarris.com/2012/10/django-a-new-way-to-write-tests/
[2]: https://github.com/dustinfarris/dustinfarris/blob/master/tests/support/utilities.py
