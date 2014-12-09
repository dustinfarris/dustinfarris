Title: "Using Google to Send Mail in Django"
Tags: Django Gmail

If you have a Gmail account (or a Google Apps account), you can use it to send mail on your behalf just like any other email client.  Remember to use port 587 (not 465), and an "application-specific" password if you use 2-step verification.

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'you@gmail.com'
EMAIL_HOST_PASSWORD = 'secret'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

The only thing interesting I've noticed here is that Google seems to disregard the "from" header and sends every email as you.

For example, attempting the following:

```python
>>> from django.core.mail import send_mail
>>>
>>> send_mail('Test', 'Test message', 'fake@yahoo.com', ['mom@gmail.com'])
```

will send the email successfully to ``mom@gmail.com``, but will come "from" ``you@gmail.com``.
