Title: "Django Media: Cleaning Up Your Mess"
Tags: Django

Sometimes it's too easy to fire and forget when it comes to setting up
FileFields in Django. Over time, a lot of media can become stale as objects
are deleted--wasting storage space. Here is a quick way to keep your waste
footprint down: Store assets for every object in a separate folder, and remove
the folder if the object is deleted. Assume the following models:

class Person(models.Model): name = models.CharField(max_length=100) class
Picture(models.Model): person = models.ForeignKey(Person) image =
models.ImageField( upload_to=lambda obj, f: 'people/%d/%s' % (obj.person.id,
f)) Note how the files are stored in an object-specific directory. Now, simply
write a pre-delete hook to remove that directory if the object is going to be
deleted:

```python
import subprocess from os.path import join from django.conf
import settings from django.db.models.signals import pre_delete from
django.dispatch.dispatcher import receiver @receiver(pre_delete,
sender=Person) def _person_delete(sender, instance, **kwargs): """Remove media
associated with a Person.""" directory = join(settings.MEDIA_ROOT, 'people',
str(instance.id)) subprocess.call(['rm', '-rf', directory])
```

