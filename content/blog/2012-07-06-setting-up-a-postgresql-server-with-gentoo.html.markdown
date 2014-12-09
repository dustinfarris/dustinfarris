Title: "Setting up a PostgreSQL Server with Gentoo"
Tags: Gentoo

Setting up a database server is usually the first step when deploying a web framework stack.  This is the second of [three documents][6] showing how to get Django up and running with Gentoo.

<a id="contents"></a>
## Contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Firewall](#firewall)
* [Install Postgres](#install-postgres)
* [Install PostGIS Extensions](#install-postgis-extensions)
* [Create Super Users](#create-super-users)
* [Conclusion](#conclusion)

<a id="introduction"></a>
## Introduction

Using Gentoo Linux to run PostgreSQL is a great marriage of technologies ready to meet and exceed the demands of most web applications.  Getting up and running is a breeze, and thanks to Gentoo's Portage packaging system, you can run multiple major versions of Postgres seamlessly on the same machine.  This document describes the basic PostgreSQL server installation requirements you should have in place when preparing to deploy a Django project.  Note this only describes the database _server_ side of Postgres.

[Contents](#contents)

<a id="prerequisites"></a>
## Prerequisites

* Gentoo Linux (see my [guide on setting up Gentoo][1])
* Root access

[Contents](#contents)

<a id="firewall"></a>
## Firewall

If Postgres will be running on a separate server from your applications, you will have to open the Postgres port on your firewall.  If Postgres is running on the same machine as your applications, you can skip this section.

Edit both ``/etc/iptables.up.config`` and ``/etc/ip6tables.up.config`` adding this line somewhere before the final "reject all" line:

```bash
# PostgreSQL server
-A INPUT -p tcp -m state --state NEW --dport 5432 -j ACCEPT
```

Save and restart iptables:

```console
iptables-restore < /etc/iptables.up.config
ip6tables-restore < /etc/ip6tables.up.config
/etc/init.d/iptables save
/etc/init.d/ip6tables save
/etc/init.d/iptables restart
/etc/init.d/ip6tables restart
```

[Contents](#contents)

<a id="install-postgres"></a>
## Install Postgres

The portage package with default USE flags is appropriate for our installation, so just emerge Postgres.

```console
emerge dev-db/postgresql-server
```

Since Django and most other web frameworks are pushing everything to be UTF-8 encoded, it's best if the database server starts doing so from the beginning.  Before creating a database, find and change (or add if missing) a line in ``/etc/conf.d/postgresql-9.1``.

```bash
PG_INITDB_OPTS="--locale=en_US.UTF-8"
```

Now create a database.  The exact command for this depends on the version of Postgres that got installed, and portage will have outputted the command needed.  If this is lost in your console history, you can always retrieve it from the logs:

```console
grep "config =dev-db/postgres" /var/log/portage/elog/summary.log
```

As of this writing, the current version of Postgres installed on a stable hardened profile is 9.1.4, so the command run is this:

```console
emerge --config =dev-db/postgresql-server-9.1.4
```

This sets up a fresh database in ``/var/lib/postgresql/9.1/`` called ``data``.  Now make any edits you need to ``/etc/postgresql-9.1/postgresql.conf``.  The defaults are probably fine, I just make sure the following are set:

```bash
lc_messages = 'en_US.UTF-8'
lc_monetary = 'en_US.UTF-8'
lc_numeric = 'en_US.UTF-8'
lc_time = 'en_US.UTF-8'
```

Finally, if this server will be separate from the application server, you will need to explicitly tell Postgres to allow connections form your application server.  In ``/etc/postgresql-9.1/postgresql.conf``, be sure that the ``listen_addresses`` variable contains the IP address postgres should listen on. e.g.:

    listen_addresses = 'localhost, 192.168.0.120'

Additional security-related configurations are found in ``/etc/postgresql-9.1/pg_hba.conf``.  If needed, add this line toward the bottom (substituting your application server's IP address):

```bash
host  all  all  156.123.456.12  trust
```

Now, just start the database server and tell Gentoo to start it on boot.

```console
/etc/init.d/postgresql-9.1 start
rc-update add postgresql-9.1 default
```

[Contents](#contents)

<a id="install-postgis-extensions"></a>
## Install PostGIS Extensions

[PostGIS][2] is a set of spatial extensions to support geographic objects in PostgreSQL.  There is a chance you may not need this right away, but it is extremely handy to have readily available when you do.  I recommend installing these extensions whether you foresee actually using them or not.

First, install the [GDAL][3] dependency:

```console
emerge gdal -avq
```

Before installing PostGIS, I find that it helps to "version lock" the installation as a major upgrade may break your applications without some TLC.  To do this, find the current version Portage is installing [here][4] and add an appropriate line to ``/etc/portage/package.mask``.  I use PostGIS 1.5.3, but PostGIS was recently upgraded to 2.0.  This breaks my applications, so I want to hold off on that upgrade for now.  I added this line to ``/etc/portage/package.mask``:

```bash
>=dev-db/postgis-2.0.0
```

which tells Portage not to install any version of PostGIS equal to or greater than 2.0.0.  Now, emerge PostGIS.

```console
emerge postgis -avq
```

As you'll probably see in the output, PostGIS requires some painless configuration before it is ready to be installed into your database.  Find and edit these two lines in ``/etc/postgis_dbs``:

```bash
templates=("template_postgis")
configured="true"
```

Install PostGIS into your database; like Postgres, the exact command here depends on the exact version of PostGIS you installed.  If you forgot, just run:

```console
grep "config =dev-db/postgis" /var/log/portage/elog/summary.log
```

For me, the command is:

```console
emerge --config =dev-db/postgis-1.5.3-r1
```

With PostGIS now installed, you will will be able to create "spatially enabled" databases using ``createdb -T template_postgis mydb``.  For more information, see the [PostGIS documentation][5].

[Contents](#contents)

<a id="create-super-users"></a>
## Create Super Users

It makes life easier if each system user using Postgres has a corresponding Postgres superuser.  The two primary users of Postgres on my machine are ``dustin`` (my personal account) and ``web`` for web applications.

```console
usermod -aG postgres dustin
usermod -aG postgres web
su - postgres
createuser -s dustin
createuser -s web
```

Now, when you switch two either of these accounts, you can run administrative commands (``createdb``, ``dropdb``, etc..) painlessly.

[Contents](#contents)

<a id="conclusion"></a>
## Conclusion

If all went well, you now have a running PostgreSQL server ready to start accepting connections.  If you have any issues getting of the ground, feel free to comment here and/or email me.

[Contents](#contents)

[1]: http://dustinfarris.com/2012/2/setting-up-a-gentoo-server/
[2]: http://postgis.refractions.net/
[3]: http://www.gdal.org/
[4]: http://gentoo-portage.com/dev-db/postgis
[5]: http://postgis.refractions.net/documentation/
[6]: http://dustinfarris.com/tag/setting-up-gentoo-postgres-and-django/
