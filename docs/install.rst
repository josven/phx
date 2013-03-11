==========================
Install PHX Django project
==========================

To use this project follow these steps:

#. Set up github
#. Get the Code
#. Create your working environment
#. Install dependencies
#. Set up project environment variables‎


Set up github
=============

To set up github follow the instructions on this page
https://help.github.com/articles/set-up-git

If you already have an github account and git installed, you can skip this step.

Get the code
============

Read this guide about how to fork a repository
https://help.github.com/articles/fork-a-repo

Use the https://github.com/josven/phx project instead of the "Spoon-Knife".


Create your working environment
===============================

You have several options in setting up your working environment.  We recommend
using virtualenv to seperate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv Only
---------------

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv --distribute phx

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Virtualenv with virtualenvwrapper
---------------------------------

In Linux and Mac OSX, you can install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/),
which will take care of managing your virtual environments and adding the
project path to the `site-directory` for you::

    $ mkdir phx
    $ mkvirtualenv -a phx phx-dev
    $ cd phx && add2virtualenv `pwd`

Windows
-------

In Windows, or if you're not comfortable using the command line, you will need
to add a `.pth` file to the `site-packages` of your virtualenv. If you have
been following the book's example for the virtualenv directory (pg. 12), then
you will need to add a python pathfile named `_virtualenv_path_extensions.pth`
to the `site-packages`. If you have been following the book, then your
virtualenv folder will be something like::

`~/.virtualenvs/phx/lib/python2.7/site-directory/`

In the pathfile, you will want to include the following code (from
virtualenvwrapper):

    import sys; sys.__plen = len(sys.path)
    /home/<youruser>/phx/phx/
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)


Installation of dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt


Set up database
===============

We use PostgreSQL in production, and I encourage to also use PostgreSQL
in developent.

For help setting up the database i refer to the PostgreSQL docuentation found
here: http://www.postgresql.org/


Set up project environment variables‎
====================================

Secret and sensetive settings are keeps out from this project.
You have to set some of the settings in you system environment variables‎.

These are the environment variables‎ you need to set.

* **PHX_SECRET_KEY** (Set this to a any random string)
* **PHX_DB_NAME**
* **PHX_DB_USER**
* **PHX_DB_PASSWORD**

Examples
--------

- On linux and osx::

	$ export PHX_SECRET_KEY=MINHEMLIGANYCKEL

- Windows systems (versions below vista)::

	> Windows key > Run > cmd.exe
	$ setx PHX_SECRET_KEY MINHEMLIGANYCKEL

- Windows system (vista and above with built-in PowerShell)::

	[Environment]::SetEnvironmentVariable("PHX_SECRET_KEY", "MINHEMLIGANYCKEL", "User")
