Title: "ImportError: cannot import name indexes"
Tags: Django

I'm certainly not the first person to hit this caveat with django-haystack, as
this error has been reported for [over a year](https://github.com/toastdriven/django-haystack/issues/315) now. However, I had trouble finding a concise
and reputable workaround. [Daniel Lindsley](https://github.com/toastdriven), the guy behind django-haystack, has alluded to a [workaround](http://django-haystack.readthedocs.org/en/v1.2.7/debugging.html#import-errors-on-start-up-mentioning-handle-registrations) in the haystack docs, but only
affirms it as the "right" fix in a [somewhat buried](https://github.com/toastdriven/django-haystack/issues/84#issuecomment-663791) GitHub issue comment. If you get
this error, it is because of the way django-haystack sets up its indexes at
the beginning of Django initialization. If there are any other applications
attempting to do something similar, it can cause conflicts and circular
imports, often leading to this error. First, instruct haystack not to load
itself on initialization: :

```python
    # settings.py ...
    HAYSTACK_ENABLE_REGISTRATIONS = False
```

Haystack cannot function without these
registrations however, so you have to "jump-start" it later in the startup
process. I chose to use urls.py. Do this for every application utilizing
haystack:

```python
    # urls.py ...
    from appname import search_indexes
```

Finally,
you'll have to modify `manage.py` so that commands like `rebuild_index` will
continue to work:

```python
    # manage.py ...
    from django.core.management import execute_from_command_line
    from projectname import search_sites
```

This is really
the only way to keep django-haystack and other apps working in harmony until
Django enhances its startup flow.
