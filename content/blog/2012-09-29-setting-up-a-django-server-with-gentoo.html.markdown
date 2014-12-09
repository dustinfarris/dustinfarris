Title: "Setting up a Django Server with Gentoo"
Tags: Django Gentoo

This is part 3 in a 3 part series I've written on setting up a Django production site on Gentoo.  In the first 2 parts I went over basic boilerplate server setup, and database installation which can be on the same server or separated.

<a id="contents"></a>
## Contents

* [Introduction](#introduction)
* [PostgreSQL](#postgresql)
* [virtualenv and pip](#virtualenv-and-pip)
* [GDAL](#gdal)
* [Basic Necessities](#basic-necessities)
* [Web User](#web-user)
* [Backups](#backups)
* [NGINX](#nginx)
* [Apache](#apache)
* [SASS](#sass)
* [Conclusion](#conclusion)

<a id="introduction"></a>
## Introduction

Django is a fantastic web framework written in Python.  It is robust, mature, and adaptable to almost any web service need.  Deploying a Django project to production can be tricky.  This guide takes you through a well-established process that I have hand-tailored to work with the Gentoo Linux operating system.

[Table of Contents](#contents)

<a id="postgresql"></a>
## PostgreSQL

Installing the PostgreSQL server is covered in [part 2](http://dustinfarris.com/2012/7/setting-up-a-postgresql-server-with-gentoo/) of this series.  If you are hosting Postgres on the same server as your Django projects, you can skip this step.  Otherwise, you'll need to install the PostgreSQL client and create an environment variable pointing to the external Postgres server:

    :::console
    emerge postgresql-base -avq

Edit ``/etc/bash/bashrc`` and add the following:

    :::bash
    export PGOST="IP of postgres server"

[Table of Contents](#contents)

<a id="virtualenv-and-pip"></a>
## virtualenv and pip

You should already know what these are for.  If you don't, this guide is not for you.

    :::console
    emerge virtualenv -avq
    easy_install pip

[Table of Contents](#contents)

<a id="gdal"></a>
## GDAL

If you plan on doing any kind of geo-locating in your projects (and you inevitably will) it is good to have this library in place.

    :::console
    echo "sci-libs/gdal geos" >> /etc/portage/package.use
    emerge gdal -avq

[Table of Contents](#contents)

<a id="basic-necessities"></a>
## Basic Necessities

All the little things.  First, make sure you've set a proper language in your make config.  This is used later when installing pyenchant for spell-checking.  Add this to the end of ``/etc/make.conf``:

    :::bash
    LINGUAS="en"

And a few other use flags you'll probably want:

    :::console
    echo "dev-vcs/subversion perl -dso" >> /etc/portage/package.use
    echo "dev-vcs/git subversion" >> /etc/portage/package.use

Time to install everything:

    :::console
    emerge sys-apps/ack mercurial subversion git pyenchant -avq
    emerge memcached xapian xapian-bindings -avq

Edit ``/etc/conf.d/memcached``:

    :::bash
    LISTENON="127.0.0.1"

Start it and set to start on boot:

    :::console
    /etc/init.d/memcached start
    rd-update add memcached default

[Table of Contents](#contents)

<a id="web-user"></a>
## Web User

This is the user that will house your projects and be responsible for Apache and NGINX.

    :::console
    useradd --create-home --system --home=/var/www web
    su - web
    cd .ssh
    ssh-keygen -t rsa -C "web@newserver"
    cd ..

Add the following to ``/var/www/.bashrc``:

    :::bash
    # Shortcut for activating a virtualenv
    alias activate='. env/bin/activate'
    # Remove all *.pyc recursively
    alias pycclean='find . -name "*.pyc" -exec rm {} \;'

And exit.

    :::console
    exit

[Table of Contents](#contents)

<a id="backups"></a>
## Backups

Ideally you'll do this on a separate server altogether, but that may not be feasible for your situation/budget.

    :::console
    useradd --create-home --system --home=/var/backups backups
    su - backups
    cd .ssh
    ssh-keygen -t rsa -C "backups@newserver"
    exit
    passwd backups

[Table of Contents](#contents)

<a id="nginx"></a>
## NGINX

We use NGINX to serve static files.  Requests for pages/services themselves get reverse-proxied to Apache which in turn will communicate with Django via WSGI.  We don't need the whole shebang with NGINX, so add the following to ``/etc/make.conf``:

    :::bash
    NGINX_MODULES_HTTP="access auth_basic autoindex browser charset empty_gif geo gzip limit_req limit_zone map memcached proxy referer rewrite split_clients ssi upstream_ip_hash userid"

And install the VIM syntax library for the NGINX configuration files (why this doesn't come with VIM by default is beyond me).

    :::console
    echo "www-servers/nginx vim-syntax" >> /etc/portage/package.use

Install NGINX.

    :::console
    emerge nginx -avq

You'll want a folder to store individual site configurations.  So create this.

    :::console
    mkdir /etc/nginx/vhosts.d

Edit ``/etc/nginx/nginx.conf`` to your liking, then start NGINX and set it to start on boot.

    :::console
    /etc/init.d/nginx start
    rc-update add nginx default

[Table of Contents](#contents)

<a id="apache"></a>
## Apache

As with NGINX, we only need parts of Apache for our purposes, so add this to ``/etc/make.conf``:

    :::bash
    APACHE2_MODULES="authz_host deflate dir filter headers include log_config logio mime mime_magic negotiation unique_id vhost_alias"
    APACHE2_MPMS="worker"

If you plan on using SSL, disregard the -ssl flags, but otherwise:

    :::console
    echo "www-servers/apache threads -ssl" >> /etc/portage/package.use
    echo "app-admin/apache-tools -ssl" >> /etc/portage/package.use

Install Apache and the WSGI mod.

    :::console
    emerge apache mod_wsgi -avq

Modify the following in ``/etc/apache2/httpd.conf``:

    :::apache
    User web
    Group web
    NameVirtualHost 127.0.0.1:8080
    Listen 8080
    Include /etc/apache2/vhosts.d/*.conf

We don't need the default virtual configs that Apache comes with, so delete them.

    :::console
    rm /etc/apache2/vhosts.d/*

And configure Apache to only load the modules we need by editing ``/etc/conf.d/apache2``:

    :::bash
    APACHE2_OPTS="-D INFO -D LANGUAGE -D WSGI"

Remove the unnecessary localhost directory (if it exists).

    :::console
    rm -rf /var/www/localhost

Start Apache and set it to start on boot.

    :::console
    /etc/init.d/apache2 start
    rc-update add apache2 default

[Table of Contents](#contents)

<a id="sass"></a>
## SASS

I use django_compressor in all of my projects which in turn compiles my SASS files for me.  If you use django_compressor in this way also, you'll need to install SASS.

    :::console
    echo 'RUBY_TARGETS="ruby19"' >> /etc/make.conf
    emerge dev-ruby/sass -avq

[Table of Contents](#contents)

<a id="conclusion"></a>
## Conclusion

If all went well, you now have a fully functional Django production stack.  Your projects can be git-cloned in the /var/www directory, then you simply need to set up the virtual environment, set up a database, collect static files, and symlink your apache and nginx configuration files to their respective vhosts.d folders.

Don't forget to set up cron jobs for backups.

If I've left anything out or failed to be clear, please let me know in the comments.
