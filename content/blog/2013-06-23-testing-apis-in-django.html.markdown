Title: "Testing APIs in Django"
Tags: [Django]
published: false

I think anyone who has got their hands more than slightly wet with functional testing knows the pain of testing code that relies on API calls.  The usual suspects can bring your tests to a screeching halt: your network is down, the API is down, the API changed.  While knowing about any of the above is important, you likely don't want a flood of emails every time the API you use has a hiccup.

Python has a few solutions to this problem.  The one I am using is also one of the simplest: [VCR.py][].  It wraps any code you like and listens for HTTP requests.  It records the responses to these requests to a file and then uses the file instead of the actual HTTP request going forward.  Awesome.

Not only does this eliminate the annoying test failures, it also speeds up the test suite overall.  Two wins for the price of one.

## What about Behavioral Tests?

Excellent question.  Turns out wrapping Selenium tests in VCR is not a good idea because it records _everything_ that is communicated over HTTP.  For Selenium that means every page request to the browser, session cookie transmission, etc..  Solution?  A little get method to replace requests.get.

First a few extra settings in ``test_settings.py``:

```python
VCR_PATH = join(TEST_DIR, 'fixtures', 'responses.yaml')
USE_VCR = True
```

And a get function in ``myproject/http.py``

```python
from django.conf import settings
import requests
import vcr


def get(*args, **kwargs):
    """Wrap HTTP requests with VCR if we are testing."""
    use_vcr = getattr(settings, 'USE_VCR', False)
    if use_vcr:
        vcr.patch.install(settings.VCR_PATH)
    response = requests.get(*args, **kwargs)
    if use_vcr:
        vcr.patch.reset()
    return response
```

Use this method from now on anywhere you would ordinarily use requests.get.

[VCR.py]: https://github.com/kevin1024/vcrpy
