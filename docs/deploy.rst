======
Deploy
======

This is an example of how phx is deployed in production in linux.

#. Prerequisites
#. Get the code with git
#. Create your production environment
#. Installation of dependencies
#. Set up database
#. Set up Apache and mod_wgsi
#. *???????*
#. Profit!

Prerequisites
=============

- git http://git-scm.com/
- virtualenv http://www.virtualenv.org/
- Apache server http://httpd.apache.org/

Get the code with git
=====================

Go were you want to have to code, example ~/phx
Then use git to clone the repository::

    $ git clone git://github.com/josven/phx.git

Create your production environment
==================================

Go were you want to have to your enviroments, example ~/env
Then create the enviroments::

    $ virtualenv --distribute phx

Installation of dependencies
=============================

Depending on where you are installing dependencies:

First make sure that you using your virtual enviroment::

    $ . ~/env/phx/bin/activate

Then install dependencies::

    $ pip install -r ~/phx/requirements/production.txt


Set up database
===============


Set up project environment variables‎
====================================

Secret and sensetive settings are keeps out from this project.
You have to set some of the settings in you system environment variables‎::

    $ export PHX_SECRET_KEY=SECRETKEY
    $ export PHX_DB_NAME=DATABASE
    $ export PHX_DB_USER=USER
    $ export PHX_DB_PASSWORD=PASSWORD

Set up Apache and mod_wgsi
==========================
