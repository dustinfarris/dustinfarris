Title: Django/Ember Authentication is Easy
Tags: [Django, Ember]

**[2013 Nov 29 Update]**: This blog examines the use of session-based authentication. You may find
token-based authentication more appropriate (as I have), in which case my more recent post will
probably better suit your needs. [Check out the latest](/2013/11/29/django-ember-token-authentication.html)

As I've [previously explained][], one of the biggest hurdles to jump when getting started with Ember
is authentication. Not anymore! I've put together a simple architecture that provides session-based
authentication in a relatively small amount of code.

[View the source on GitHub][]

## Session-based Authentication

If you Google "Ember authentication" you'll likely get a handful of SO posts and an even smaller handful
of blog posts almost all of which implement some kind of token-based authentication, usually relying on
Rails or Node for authentication. This requires you to perform a back-and-forth exchange with the server
to authenticate credentials and receive a token. You probably have to store the token in some kind of
manually made cookie or local-based storage, and you have to remember to consistently provide the token
whenever you access a restricted resource.

Session-based authentication is a lot easier! The concept of session-based authentication is very similar
to token-based authentication but with some important differences. First, the server-side mechanics for 
session-based auth are entirely built in to Django. Second, because the majority of the work is done server-
side, there is little required of you in Ember. As with token-based authentication, though, it is important
to remember that after authentication, subsequent requests will contain a session-id cookie—consider using
SSL to encrypt client-server communication.

REST purists might argue that session-based authentication is technically not "stateless."  The trade-off
depends on project requirements and personal preference.  For single-page web applications, I can't think
of any practical downsides.

## Architecture

The basic design consists of a SessionController in Ember, and a SessionView in Django. While not required,
I'm also throwing in a User model in Ember and UserSerializer in Django to facilitate the notion of the
"current user" in Ember.

The SessionController is responsible for providing login/logout actions, and maintaining an accurate
manifestation of the current user (or lack thereof). To make this simple, I made the 'model' property of the
SessionController an instance of User.

The SessionView is responsible for providing the currently logged-in user (if one exists), authenticating
a new user, and logging a user out. Each of these operations are distinguished by a GET, POST, or DELETE
HTTP request respectively.

I use a single handlebars template to provide the login form, and then replace that form with a welcome
message when the user authenticates.  This welcome message could be replaced with a link to the user's profile.

## Code

When the user successfully authenticates, the SessionView returns a success flag and, as a bonus, the user's
id. Ember can then use the user id to pull information about the current user. To do that we need a serializer
and a ViewSet.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
```

With that out of the way, we can focus on authentication.  On the server side we need a SessionView that can
handle logging in, logging out, and returning the current user if one exists. We also want it to return an
appropriate error message if authentication fails:

```python
class SessionView(APIView):
    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def _error_response(self, message_key):
        data = {
            'success': False,
            'message': self.error_messages[message_key],
            'user_id': None,
        }
        return Response(data)

    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return Response({'user_id': request.user.id})
        return Response({'user_id': None})

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'success': True, 'user_id': user.id})
            return self._error_message('disabled')
        return self._error_message('invalid')

    def delete(self, request, *args, **kwargs):
        # Logout
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
```

And we just need to expose the user API and the session view in urls.py:

```python
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns('',
    url(r'^session/$', SessionView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^', TemplateView.as_view(template_name='application.html')),
)
```

That takes care of the server side of things.  In Ember we'll need a User model:

```js
var attr = DS.attr;

App.User = DS.Model.extend({
  username: attr(),
  first_name: attr(),
  last_name: attr()
});
```

The SessionController in Ember takes care of sending the user-provided credentials to the server, sending a
logout request to the server, or retrieiving the current user. Specifically, we need a way to reset the
controller's values, a flag that represents whether there is currently an authenticated user, and login/logout
actions:

```js
App.SessionController = Ember.ObjectController.extend({
  username: null,
  password: null,
  errorMessage: null,

  reset: function() {
    this.setProperties({
      username: null,
      password: null,
      errorMessage: null,
      model: null
    });
  },

  isAuthenticated: function() {
    return !Ember.isEmpty(this.get('model'));
  }.property('model'),

  setCurrentUser: function(user_id) {
    if (!Ember.isEmpty(user_id) {
      var currentUser = this.store.find('user', user_id);
      this.set('model', currentUser);
    }
  },

  actions: {
    login: function() {
      var self = this, data = this.getProperties('username', 'password');
      $.post('/session/', data).then(function(response) {
        self.set('errorMessage', response.message);
        self.setCurrentUser(response.user_id);
      });
    },
    logout: function() {
      $.ajax({url: '/session/', type: 'delete'});
      this.reset();
      this.transitionToRoute('index');
    }
  }
});
```

We then do an initial "current user" query in the main application router to check if there is already an active
session when the page is first loaded:

```js
App.Router.map(function() {
  this.resource('session');
});

App.ApplicationRoute = Ember.Route.extend({
  setupController: function(controller, model) {
    var self = this;
    Ember.$.getJSON('/session/').then(function(response) {
      self.controllerFor('session').setCurrentUser(response.user_id);
    });
  }
});
```

Finally we just need a handlebars template to provide the user with a login form, or with a representation of
the current user.

{% raw %}
```html
<script type="text/x-handlebars" id="session">
  {#if isAuthenticated}}
    <h3>Welcome back, {{first_name}}!</h3>
    <button {{action 'logout'}}>Logout</button>
  {{else}}
    <form {{action login on="submit"}}>
      {{input value=username type="text" placeholder="Username"}}
      {{input value=password type="password" placeholder="Password"}}
      {{input value="Login" type="submit"}}
    </form>
    {{#if errorMessage}}<span>{{errorMessage}}</span>{{/if}}
  {{/if}}
</script>
```
{% endraw %}

You can put this login form wherever you want by calling {% raw %}``{{render 'session'}}``{% endraw %}.

## Conclusion

Authenticating in Ember using Django's session-based authentication is straight-forward and easy.  I've left
out a lot of boiler-plate and tests here. You can view a more complete and working [example on GitHub].


[previously explained]: /2013/08/authenticating-django-slash-ember/
[View the source on GitHub]: https://github.com/dustinfarris/django-ember-authentication
[example on GitHub]: https://github.com/dustinfarris/django-ember-authentication

