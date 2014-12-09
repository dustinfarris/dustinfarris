Title: Authenticating Django/Ember
Tags: [Django,Ember]

**[2013 Sep 21 Update]**: I've completely refactored this solution and have done a much better job of
implementing it and explaining it.  [Check out the latest](/2013/11/29/django-ember-authentication-is-easy.html)

******************************************

The web app rage nowadays is to implement your backend as RESTfully as possible, and use Javascript frameworks to facilitate your controller and presentation layers as a single-page application.  There is bit of a learning curve involved when adapting to the new philosophies—especially so because the frameworks are still in their infancy.

Currently, I'm using Django 1.6 (beta) for the ORM, [Django Rest Framework][] to handle HTTP requests, and [Ember][] on the client side.

To date, the biggest hurdle I've had to jump is authenticating a user, and then polling for a currently authenticated user.  There are a [few methodologies][] that could be considered given the technologies I'm using.  They include:

* Basic Auth
* Token Auth
* Session Auth
* OAuth(2)

I chose to implement **Session Auth** because it works with Django out of the box, and turned out to be mostly painless to implement on the Ember side.

I created a `users` application in Django, partly because I needed to [extend the User model][] to satisfy a few project requirements, and partly because I wanted to namespace the tasks involving authentication.  To keep things simple, let's say my model looked something like this:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.IntegerField()
```

Nothing complex.  The bulk of what we need is inherited straight out of Django.

Then I made a quick serializer for DRF:

```
from reset_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'age')
```

Again, basic stuff.

The tricky part was deciding how to **A**) authenticate the user "RESTfully" (which is really an incongruous thing to say—but for lack of better terms...), and **B**) return the currently authenticated user.

I chose to do all of it in one view (well two including the standard DRF ViewSet), borrowing logic from a few Django built-ins like the AuthenticationForm:

```python
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

@api_view(['POST', 'GET', 'DELETE'])
def session(request):
    """
    Handle "RESTful" login, logout, get current user
    """
    # Login
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.DATA)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(form.errors)

    # Logout
    elif request.method == 'DELETE':
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    # Get currently authenticated user's id
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return Response({'user_id': request.user.id})
        return Response({}, status=status.HTTP_204_NO_CONTENT)
```

And for completeness, here is `urls.py`:

```python
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'api/', include(router.urls),
    url(r'session/', 'users.views.session'),
    url(r'^', TemplateView.as_view(template_name="site.html")),
)
```

Now the tricky part comes in tying it all together in Ember.  Skipping the HTML5 boilerplate for brevity, here's the contents of the `<body>` tag inside `site.html`:

{% raw %}
```html
<script type="text/x-handlebars">
  <header>
    {{render 'session'}}
  </header>
  <div id="main">
    {{outlet}}
  </div>
</script>

<script type="text/x-handlebars" data-template-name="session">
  <div id="user">
    {{#if authenticated}}
      Welcome back, {{content.firstName}}!
      <a href="#" {{action 'logout'}}>Logout</a>
    {{else}}
      {{#linkTo 'sessions.new'}}Login{{/linkTo}}
    {{/if}}
  </div>
</script>

<script type="text/x-handlebars" data-template-name="sessions/new">
  <form {{action 'login' on="submit"}}>
    <h2>Login</h2>
    {{#if allError}}<div class="error">{{allError}}</div>{{/if}}
    {{#if usernameError}}<div class="error">{{usernameError}}{{/if}}
    {{input value=username type="text" placeholder="Username"}}
    {{#if passwordError}}<div class="error">{{passwordError}}{{/if}}
    {{input value=password type="password" placeholder="Password"}}
    {{input type="submit" value="Login"}}
  </form>
</script>
```
{% endraw %}

Finally, in the Ember code I had to automate the check for a currently logged-in user, and provide the logic for logging in and out.  Here is `application.coffee`:

```coffeescript
# Application

window.App = Ember.Application.create()


# Store

App.Store = DS.DjangoRESTStore.extend
  revision: 1
  adapter: DS.DjangoRESTAdapter.extend
    url: '/api'


# Router

App.Router.map ->
  @resource "users"
  @resource "sessions", ->
    @route "new"

App.ApplicationRoute = Ember.Route.extend
  setupController: (controller, context) ->
    @controllerFor('session').update()


# Models

App.User = DS.Model.extend
  firstName = DS.attr('string')
  lastName = DS.attr('string')
  email = DS.attr('string')
  age = DS.attr('number')

App.Session = DS.Model.extend
  user: DS.belongsTo('App.User')


# Controllers

App.ApplicationController = Ember.Controller.extend
  user: Ember.computed.alias 'controllers.session.content'

App.SessionController = Ember.Controller.extend
  content: null
  authenticated: false
  init: ->
    @_super()
    @update()
  update: ->
    # Check if there is a user logged in already
    $.get('/session/').then (response) =>
      if !Ember.isEmpty(response) and !Ember.isEmpty(response.user_id)
        @set 'content', App.User.find(response.user_id)
        @set 'authenticated', true
      else
        @set 'content', null
        @set 'authenticated', false
  logout: ->
    $.ajax(url: '/session/', type: 'DELETE').then (response) =>
      @controllerFor('session').update()
      @transitionToRoute('index')

App.SessionsNewController = Ember.Controller.extend
  login: ->
    data = @getProperties 'username', 'password'
    $.post('/session/', data).then (response) =>
      if (response.id)  # Success
        @controllerFor('session').update()
        @transitionToRoute('index')
      else
        @set('allError', response.__all__)
        @set('usernameError', response.username)
        @set('passwordError', response.password)
```

There you have it.  Anywhere else in the application you can refer to `controllerFor('session').get('content')` to access the logged-in user.


[Django Rest Framework]: http://django-rest-framework.org/
[Ember]: http://emberjs.com/
[few methodologies]: http://django-rest-framework.org/api-guide/authentication.html#api-reference
[extend the User model]: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
