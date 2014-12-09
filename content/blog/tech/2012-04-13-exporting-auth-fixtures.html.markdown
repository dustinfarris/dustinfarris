Title: "Exporting `auth` Fixtures"
Tags: Django

I've discovered, rather painfully, that setting up auth fixtures for testing
requires a little care. Problems result when South
migrations interfere with fixture permissions.

The best way to dump auth data is to use natural keys and avoid the permission
model altogether:

    
    ./manage.py dumpdata -n auth.user auth.group > auth.json


