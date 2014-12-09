Title: "Testing Management Commands"
Tags: Django

I think to be a good Django citizen it would be appropriate to write tests ensuring that standard management commands work with your application.  I thought of this after dealing with a [certain app][1] that doesn't handle ``loaddata`` very well.

Going forward, I'm adding this TestCase to all of my applications:

```python
from os.path import join
import subprocess

from django.conf import settings
from django.core import management


class TestManagement(TestCase):
    fixtures = ['myapp']

def setUp(self):
    self.project_dir = getattr(settings, 'PROJECT_DIR', None)
    if self.project_dir is None:
        raise ImproperlyConfigured('Missing PROJECT_DIR in settings')

def tearDown(self):
    subprocess.call(['rm', join(self.project_dir, 'test_myapp.json')])

def test_dumpdata_loaddata(self):
    data_file = open(join(self.project_dir, 'test_myapp.json'), 'w')
    management.call_command('dumpdata', 'myapp', stdout=data_file)
    data_file.close()
    management.call_command('loaddata', join(self.project_dir, 'test_myapp.json'))
```

It's a little awkward because I'm relying on the test throwing an error rather than failing an assertion, but it's the best my 10pm mind can come up with for now.

[1]: https://github.com/divio/django-cms/
