Title: "Virtual Hosting, Rails, NGINX, Apache, Passenger, Ubuntu"
Tags: [Ruby on Rails]

I've become a fan of [RVM][1], which allows you to create pseudo virtual environments called "gemsets" that can be version-locked to the specific needs of your individual projects.  In Rails, deploying several of these projects to a single server can be tricky.  This tutorial describes how this can be done.

<a id="contents"></a>
## Contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Server setup](#server-setup)
* [Dependencies](#dependencies)
* [Configure MySQL](#configure-mysql)
* [Create Web user](#web-user)
* [Install RVM](#install-rvm)
* [Install Passenger](#install-passenger)
* [Configure Apache](#configure-apache)
* [Configure NGINX](#configure-nginx)
* [Deploy your project](#deploy-your-project)
* [Conclusion](#conclusion)

<a id="introduction"></a>
## Introduction

Setting up a server to host multiple Ruby on Rails projects requires a well thought-out strategy to ensure a responsive system that meets your various needs.  NGINX has a fantastic record for serving static content.  Apache and Passenger are workhorses that form a terrific relationship with Ruby on Rails.  We'll combine the best of these programs to serve multiple Rails projects on an Ubuntu server.

[Table of Contents](#contents)

<a id="prerequisites"></a>
## Prerequisites

You will need:

* Ubuntu (I am using 12.04 LTS)
* Root access or the ability to run ``sudo`` commands
* A Rails project (or several)

[Table of Contents](#contents)

<a id="server-setup"></a>
## Server setup

These are a few basic boiler-plate Ubuntu things you may have done already:

    :::console
    locale-gen en_US.UTF-8
    /usr/sbin/update-locale LANG=en_US.UTF-8
    dpkg-reconfigure tzdata
    apt-get update && apt-get upgrade
    reboot

[Table of Contents](#contents)

<a id="dependencies"></a>
## Dependencies

A few libraries that you'll want.  We'll also install NGINX, Apache, and MySQL here so they're in place when we configure them later.  Modify this list as needed--for example if you use subversion instead of git.

    :::console
    apt-get install build-essential git-core
    apt-get install htop libssl-dev libreadline5 libreadline5-dev curl zlib1g zlib1g-dev
    apt-get install libcurl4-gnutls-dev libopenssl-ruby apache2-prefork-dev libapr1-dev libaprutil1-dev
    apt-get install libxslt-dev libxml2-dev nodejs npm
    apt-get install apache2
    apt-get install nginx
    apt-get install mysql-server mysql-client

[Table of Contents](#contents)

<a id="configure-mysql"></a>
## Configure MySQL

I like to create a ``web`` MySQL to coincide with the ``web`` system user we'll create later.  All my Rails projects use the ``web`` MySQL user in production.  Tune to fit your own requirements if needed.

    :::mysql
    mysql -u root

    CREATE USER web;
    GRANT ALL ON *.* TO 'web';
    FLUSH PRIVILEGES;

[Table of Contents](#contents)

<a id="web-user"></a>
## Create Web user

We'll create a system user to contain all Rails applications in the ``/var/www`` directory.  Afterwords, create your RSA key needed for GitHub and others.

    :::console
    rm -rf /var/www
    adduser --system --shell=/bin/bash --home=/var/www web
    addgroup web
    usermod -g web web
    su - web
    mkdir .ssh
    chmod 700 .ssh
    cd .ssh
    ssh-keygen -t rsa -C "web@rails"
    cd

Create the [ractivate][2] script in the web user's home directory.  Once done, add the following to ``.bashrc``:

    :::bash
    alias ractivate='source ~/.ractivate'
    export RAILS_ENV='production'

Create ``.gemrc`` in the web user's home directory and add the following:

    :::bash
    install: --no-rdoc --no-ri
    update: --no-rdoc --no-ri

[Table of Contents](#contents)

<a id="install-rvm"></a>
## Install RVM

Run the following, as the web user, to install RVM.  This will take a while.

    :::console
    curl -L https://get.rvm.io | bash -s stable --ruby

When that finishes, install Ruby (1.9.3 for me), create a global gemset, and install bundler.

    :::console
    rvm install 1.9.3 --with-openssl-dir=~/.rvm/
    rvm gemset use 1.9.3@global --create --default
    gem install bundler

[Table of Contents](#contents)

<a id="#install-passenger"></a>
## Install Passenger

Passenger acts as the liaison between Ruby and Apache.  It is very quick, easy to install, and has [fantastic documentation][3].  Install with the following command, but do not follow the instructions it gives to configure Apache.  We'll do that later in a slightly modified way to accomodate multiple gemsets.

    :::console
    gem install passenger
    rvm wrapper 1.9.3@global passenger
    passenger-install-apache2-module

[Table of Contents](#contents)

<a id="#configure-apache"></a>
## Configure Apache

Now we have to make Apache work with our web user and Passenger.  Switch back to your ``root`` user and change the following variables in ``/etc/apache2/envvars``

    :::bash
    export APACHE_RUN_USER=web
    export APACHE_RUN_GROUP=web

To load the Passenger module, add the following to ``/etc/apache2/httpd.conf``.  **Modify this for the version of Ruby and Passenger you installed.**

    :::apache
    LoadModule passenger_module /var/www/.rvm/gems/ruby-1.9.3-p194@global/gems/passenger-3.0.15/ext/apache2/mod_passenger.so
    PassengerRoot /var/www/.rvm/gems/ruby-1.9.3-p194@global/gems/passenger-3.0.15
    PassengerRuby /var/www/.rvm/bin/passenger_ruby

Configure Apache to listen locally on port 8080 by changing the following in ``/etc/apache2/ports.conf``

    :::apache
    NameVirtualHost 127.0.0.1:8080
    Listen 8080

Restart Apache.

    :::console
    service apache2 restart

[Table of Contents](#contents)

<a id="configure-nginx"></a>
## Configure NGINX

NGINX is almost ready to go out of the box; you'll just need to create a proxy configuration.  Create ``/etc/nginx/proxy.conf`` and paste the following:

    :::nginx
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Url-Scheme $scheme;
    client_max_body_size 10m;
    client_body_buffer_size 128k;
    proxy_connect_timeout 90;
    proxy_send_timeout 90;
    proxy_read_timeout 90;
    proxy_buffers 32 4k;

    # vim: ts=4 ft=nginx

Restart NGINX.

    :::console
    service nginx restart

[Table of Contents](#contents)

<a id="deploy-your-project"></a>
## Deploy your project

Before deploying to the server you will need 3 project-specific configuration files.

### Project Apache config

Create ``/etc/apache2/sites-available/projectname.conf`` and add the following (modified for your project):

    :::apache
    <VirtualHost 127.0.0.1:8080>
    	ServerName projectname.com

    	DocumentRoot /var/www/projectname/public

        <IfModule mod_rpaf.c>
            RPAFenable On
    	    RPAFsethostname On
            RPAFproxy_ips 127.0.0.1
        </IfModule>

        LogLevel warn
        CustomLog /var/log/apache2/projectname.access.log combined
        ErrorLog /var/log/apache2/projectname.error.log
    </VirtualHost>

    # vim: ft=apache

### Project NGINX config

Create ``/etc/nginx/sites-available/projectname.conf`` and add the following (modified for your project):

    :::nginx
    server {
        listen 80;
        server_name projectname.com;

        access_log  /var/log/nginx/jdknot.access.log;
        error_log   /var/log/nginx/jdknot.error.log;

        location /assets {
            alias /var/www/projectname/public/assets;
        }

        location / {
            proxy_pass http://localhost:8080;
            include /etc/nginx/proxy.conf;
        }
    }

    # vim: ft=nginx

### Project setup_load_paths config

This is a file you'll add to your Rails project to inform Passenger about your gemset.  On your local machine, create ``projectname/config/setup_load_paths.rb`` and paste the following:

    :::ruby
    if ENV['MY_RUBY_HOME'] && ENV['MY_RUBY_HOME'].include?('rvm')
    	begin
    	    rvm_path = File.dirname(File.dirname(ENV['MY_RUBY_HOME']))
    	    rvm_lib_path = File.join(rvm_path, 'lib')
    	    $LOAD_PATH.unshift rvm_lib_path
    	    require 'rvm'
    	    RVM.use_from_path! File.dirname(File.dirname(__FILE__))
        rescue LoadError
    	    raise "RVM ruby lib is currently unavailable."
        end
    end

    ENV['BUNDLE_GEMFILE'] = File.expand_path('../Gemfile', File.dirname(__FILE__))
    require 'bundler/setup'

And create a rvmrc file to points to your gemset.  Create ``projectname/.rvmrc`` and add:

    :::bash
    rvm 1.9.3@projectname

If you haven't already done so, commit these changes.

    :::console
    git add config/setup_load_path.rb
    git add .rvmrc
    git commit -m "Created setup_load_path and rvmrc"
    git push

### Clone and setup project

Back on the server, as your web user: clone your project, setup a gemset, and prepare the database and assets:

    :::console
    su - web
    git clone git@github.com:yourname/projectname.git
    rvm gemset create projectname
    cd projectname
    ractivate
    bundle install --binstubs
    rake db:create
    rake db:migrate
    rake assets:precompile

### Restart Apache and NGINX

As root:

    :::console
    service apache2 restart
    service nginx restart

[Table of Contents](#contents)

<a id="conclusion"></a>
## Conclusion

If all went well, you should be able to load projectname.com.  If things don't work right, good places to start debugging are the log files in ``/var/log/apache/`` and ``/var/log/nginx/``.  As always, feel free to comment or [contact me][4] if I have failed to explain anything clearly.

A huge thanks to Aaron Sumner for his blog on [using Passenger with RVM][5].

[1]: https://rvm.io/
[2]: /2012/8/ractivate-the-missing-script-for-rvm/
[3]: http://www.modrails.com/documentation.html
[4]: /contact/
[5]: http://everydayrails.com/2010/09/13/rvm-project-gemsets.html
