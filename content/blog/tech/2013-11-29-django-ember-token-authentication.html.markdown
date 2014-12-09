Title: Django/Ember Token Authentication
Tags: Django, Ember
Summary: "Authentication can be a real headache. Thankfully, Django REST Framework and Ember have taken care of the heavy-lifting already."

As I've [previously detailed](/2013/09/21/django-ember-authentication-is-easy.html), 
implementing session-based authentication with Django and Ember is not as hard as you might think.
Now I'd like to say the same thing for token-based authentication.

In token-based authentication, every user in the database is assigned a unique token.  The flow of 
authentication then works like this:

1. You send a username and password to the API
2. The API validates the credentials and returns that user's token
3. You include the token in the header of every request going forward to prove that you are already 
   authenticated.

Here's a demonstration of the concept using curl:

    $ curl localhost:8000/users/
    {"detail": "Authentication credentials were not provided."}

    $ curl -X POST -d "username=bob&password=correct" localhost:8000/api-token-auth/
    {"token": "abcdefg12345"}

    $ curl -H "Authorization: Token abcdefg12345" localhost:8000/users/
    [{"id": 1, "username": "bob", "email": "bob@example.org"}]

Here, I'll explain how to set up token-based authentication using Django REST Framework, and how to 
set up Ember as a consumer.  I'll assume you already have DRF installed, and that you have [extended 
Django's User model](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model) 
(which I really recommend you do from the beginning even if you don't have an immediate need), e.g.:

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```

## Django (DRF)

After installing DRF in the usual way, you will want need a way to generate tokens for your users, 
and return them when a consumer posts valid credentials.  Fortunately, DRF has most of this 
functionality [built in](http://django-rest-framework.org/api-guide/authentication#tokenauthentication).  
First, add `rest_framework.authtoken` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'rest_framework.authtoken',
)
```

Run `manage.py syncdb`.  Refer to the [DRF documentation](http://django-rest-framework.org/api-guide/authentication#schema-migrations) 
for possible edge cases involving South migrations.  Finally, create tokens for all existing users 
in the Python shell:

```python
from rest_framework.authtoken.models import Token
from users.models import User
for user in User.objects.all():
    Token.objects.create(user=user)
```

### Automating token creation

Going forward, you'll want to automate the creation of tokens for new users.  This is easily 
achieved with a post_save hook for the User model.

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def init_new_user(sender, instance, signal, created, **kwargs):
    """
    Create an authentication token for newly created users.
    """
    if created:
        Token.objects.create(user=instance)
```

### Authentication endpoint

DRF takes care of authenticating credentials and returning a token.  You just need to add the 
endpoint to your URLconf:

```python
urlpatterns += patterns('',
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
```

### Token-based policy

The last piece as far as Django is concerned is specifying that you want to use token-based 
authentication throughout your REST API.  This can be done by adding/modifying the 
`DEFAULT_AUTHENTICATION` setting:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # optional
    ),
}
```

I keep SessionAuthentication for using the web-browsable API that DRF comes with.

### The current user

Thinking ahead, we know that in Ember, after authenticating, we will want an easy way to retrieve details 
about the authenticated user.  Things like, name, email, etc..  The DRF response to a correct username 
and password is: a token.  While the token helps us authenticate future requests, it tells us nothing
about the user we just authenticated.  We can't even do a GET request to /users/:id/ because we don't
even know what the user's ID is!  To solve this problem, I like to create a special endpoint that returns 
the currently authenticated user at /users/me/.  This is easy to accomplish in DRF.  In your UserViewSet:

```python
class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if pk == 'me':
            return Response(UserSerializer(request.user).data)
        return super(UserViewSet, self).retrieve(request, pk)
```

That's it for setting up Django.

## Ember

As explained above, to make use of token authentication, we'll need to send a username and password 
to the API, store the returned token, and provide the token in the header for any future request to 
the API.  In short, we need:

* A user model to store user data
* An authentication controller to facilitate the exchange of credentials for a token and store the 
  currently authenticated user
* A way to prevent an unauthenticated user from visiting protected pages

The model is straight-forward:

```js
App.User = DS.Model.extend({
    username: DS.attr(),
    first_name: DS.attr(),
    last_name: DS.attr(),
    email: DS.attr(),
    is_active: DS.attr('boolean')
});
```

Of course your model may be different depending on how you've extended the User Django model.

### AuthController

The real meat of token authentication in Ember lies in a controller we'll create to submit form 
information (username/password) to the server, retrieve the token, store the token, and provide 
information about the currently logged in user.  To accomplish this, we'll extend ObjectController, 
so that the controller itself represents the logged in user (or lack thereof).  Remember that 
ObjectControllers in Ember are manifestations of a model—just as ArrayControllers are manifestations 
of a set of models, etc.

```js
App.AuthController = Ember.ObjectController.extend();
```

I'm going to digress and talk for a second on Django, Ember, and forms.  In Ember, form fields can 
be tied to controller attributes.  In Django, forms are validated and if they are not valid, a set 
of errors is returned.  In this case we will be submitting form data to Django REST Framework which 
passes the information on to the UserSerializer for validation.  Serializers in DRF inherit from 
Django forms, so the errors we get back (if any) will look just like errors we might get back from 
an invalid Django form.  So we know that errors will come back as a Python dictionary, converted to 
a JSON object, e.g.:

```json
{"username": "This field is required."}
```

or 

```json
{"non_field_errors": "Invalid username or password"}
```

We are going to use these ideas to our advantage to submit form data to Django, and report back 
with any errors (like an invalid password).

So right now we have an AuthController that does nothing.  It has a "model" attribute, which we will 
use later on to represent the currently logged in user.  We are going to add a few more attributes 
to represent the form fields we need, the token we eventually get back, and any errors encountered 
while processing the login form.

```js
App.AuthController = Ember.ObjectController.extend({
    username: null,
    password: null,
    token: null,
    errors: null,
    reset: function() {
        this.setProperties({
            username: null,
            password: null,
            errors: null,
            model: null
        });
    }
});
```

Let's look at the authentication handlebars template we'll be using:

```hbs
<form {{action 'login' on='submit'}}>
    <div {{bind-attr class='errors.username:has-error'}}>
        <span>{{errors.username}}</span>
        {{input value=username type='text' placeholder='Username'}}
    </div>
    <div {{bind-attr class='errors.password:has-error'}}>
        <span>{{errors.password}}</span>
        {{input value=password type='password' placeholder='Password'}}
    </div>
    {{#if errors.non_field_errors}}
    <div>
        <strong>Oops!</strong> {{errors.non_field_errors}}
    </div>
    {{input type='submit' value='Log in'}}
</form>
```

Easy: we have a username and password field bound to the AuthController, and a few areas of text 
that are bound to any potential errors we get back.  When the form is submitted, the "login" action 
is fired, so let's implement that in the controller:

```js
...
actions: {
    login: function() {
        var self = this;
        var data = this.getProperties('username', 'password');
        $.post('/api-token-auth/', data, null, 'json').then(
            function(response) {
                self.reset();
                self.set('token', response.token);
                self.transitionToRoute('index');
            },
            function(jqXHR, status, error) {
                self.set('errors', $.parseJSON(jqXHR.responseText));
            }
        );
    }
}
...
```

If the authentication request is successful, we'll reset the form (a function we'll implement later 
to just clear the fields of their old values), store the token, and navigate to the index (or 
wherever you want the user to go next).  If the authentication request is not successful, we'll 
populate the errors attribute so the user gets information on why the form was not valid.

**The tricky part!**  After the authentication request to the API succeeds, we want to 
store the token permanently (so if the user refreshes the page, they are still logged in), _and_ we 
want to make sure that any future API request includes the token in the header.  To accomplish the 
latter we'll implement functions in the AuthController to check for a valid token, setup future AJAX 
requests to use the token, retrieve the current user, and process a new token when it is set by a 
successful authentication form response:

```js
...
hasValidToken: function() {
    var token = this.get('token');
    return (!Ember.isEmpty(token) && token != 'null' && token !== 'undefined');
}.property('token'),
setupAjax: function() {
    var self = this, token = this.get('token');
    $(document).ajaxSend(function(event, xhr, settings) {
        if (self.hasValidToken()) {
            xhr.setRequestHeader("Authorization", "Token " + token);
        }
    });
},
setCurrentUser: function() {
    if (this.hasValidToken()) {
        var currentUser = this.store.find('user', 'me');
        this.set('model', currentUser);
    } else {
        this.reset();
    }
},
tokenChanged: function() {
    localStorage.MYPROJECT_auth_token = this.get('token');
    this.setupAjax();
    this.setCurrentUser();
}.observes('token')
...
```

Here we have an observer that persists a new token to local storage, sets up future AJAX requests, 
and retrieves the currently logged in user.

### Retrieving tokens from local storage

You'll notice above that we persist the token to local storage.  This is so the token is still 
available even if the user refreshes the page (or leaves and comes back, etc..)  We'll need to 
retrieve the token from local storage anytime the user visits the site, so create/modify 
ApplicationRoute to handle this.  While we're at it, we'll add a 'logout' action that can be 
accessed from anywhere in the site:

```js
App.ApplicationRoute = Ember.Route.extend({
    init: function() {
        this._super();
        this.controllerFor('auth').set('token', localStorage.MYPROJECT_auth_token);
        this.controllerFor('auth').setupAjax();
        this.controllerFor('auth').setCurrentUser();
    },
    actions: {
        logout: function() {
            App.reset();
            this.controllerFor('auth').set('token', null);
            this.transitionTo('index');
        }
    }
});
```

If the user has not visited the site before, or has not authenticated, 
`localStorage.MYPROJECT_auth_token` will return `undefined`.

### Protected Routes

Invariably, there will be some routes you do not want unauthenticated users to access.  We'll 
create a base route that covers these:

```js
App.RestrictedRoute = Ember.Route.extend({
    beforeModel: function(transition) {
        if (!this.controllerFor('auth').hasValidToken()) {
            this.transitionTo('auth');
        }
    }
});
```

And all other protected routes will extend this, e.g.:

```js
App.MySecretRoute = App.RestrictedRoute.extend({ …
```

### Tying it all together

So now we have an AuthController, an auth template, and a few modifications to our routes.  All 
that's remaining is creating the actual login page, and a way to get to it.  In your router:

```js
App.Router.map(function() {
    this.route('auth', { path: '/login' });
});
```

This will use the auth template and controller we already created, now we just need part of the 
main application template to provide information about the logged in user, or provide a link to 
the login page if the user is not yet logged in.  To do this we'll need to make the AuthController 
available to the main application template.  So create/modify ApplicationController:

```js
App.ApplicationController = Ember.Controller.extend({
    needs: 'auth'
});
```

And now in your main application handlebars template:

```hbs
{{#with controllers.auth}}
{{#if hasValidToken}}
Welcome back, {{first_name}} {{last_name}}!
<a href="#" {{action 'logout'}}>Logout</a>
{{else}}
{{#link-to 'auth'}}Login{{/link-to}}
{{/if}}
{{/with}}
```

## Conclusion

Everything above, when put together, will provide you with a token-based authentication scheme for 
your API server, and a way to consume it using Ember.  Token-based authentication is nice because 
it is straight-forward for other API consumers to plug into quickly without having to worry about 
cookies and such.  Think mobile applications.

Remember, the initial request to retrieve a token sends a plain text username and password across 
the net, and all subsequent requests send a naked token across the net.  Always use SSL when using 
token-based authentication.
