Title: "Why RoR is Awesome (part 1 of many)"
Tags: [Ruby on Rails]

I finally took the plunge.  I'm learning Rails.  And holy shit.

RoR has a philosophy of being RESTful, which means using what's already built (HTTP) rather than reinventing the wheel.

I launched a "users" app using just these _three_ commands taken from the tutorial I'm following:

```console
rails generate scaffold User name:string email:string
rake db:migrate
rails server
```

With _no further modifications_, check this out (truncated for brevity):

```console
> telnet localhost 3000

> POST /users HTTP/1.0
> Content-Length: 57
>
> user[name]=Dustin&user[email]=dustin@dustinfarris.com
<html><body>You are being <a href="http://localhost:3000/users/1">redirected</a>.</body></html>

> GET /users.json
[{"id":1,"name":"Dustin","email":"dustin@dustinfarris.com"}]

> GET /users/1.json
{"id":1,"name":"Dustin","email":"dustin@dustinfarris.com"}

> DELETE /users/1
<html><body>You are being <a href="http://localhost:3000/users">redirected</a>.</body></html>

> GET /users.json
[]
```

This is exciting stuff I tell you.  And I'm only on [chapter 2][1]!

[1]: http://ruby.railstutorial.org/
