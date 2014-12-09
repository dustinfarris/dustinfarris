Title: "The Longest Shell Command I've Written"
Tags: Bash

I keep two (or more) versions of PostgreSQL installed on my laptop that I
switch between depending on what project I'm working on. In
Snow Leopard, this involved setting the path for postgres to whatever version
I was using. In Lion however, it is easier to switch the
home directory for postgres altogether; leading to an alias containing this
command:

```bash
dscl localhost -change /Local/Default/Users/postgres NFSHomeDirectory `dscl localhost -read /Local/Default/Users/postgres NFSHomeDirectory | grep '/.*' -o` /opt/local/var/db/postgresql91
```

That's one command, and likely the longest I've personally written!


