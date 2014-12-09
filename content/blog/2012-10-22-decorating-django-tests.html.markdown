Title: "Decorating Django Tests"
Tags: Django Python

Just a quick note: when decorating Django tests you have to take care to name your return function using the same "test_" format otherwise an unmodified TestRunner will not discover it.

This will work:

```python
def mydecorator():
  def wrapper(f):
    def test_func(*args, **kwargs):
      # Do some stuff
      result = f(*args, **kwargs)
      return result
    return test_func
  return wrapper


class TestMath(TestCase):

  @mydecorator
  def test_addition(self):
    self.assertEqual(1 + 1, 2)
```

Note the innermost function in the decorator is named "test_func."  If this was named something more conventional, like "func," the decorated test would not be discovered.
