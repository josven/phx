==========================
Install PHX Django project
==========================

To use this project follow these steps:

#. Install Python 2.7
#. Set up github
#. Get the Code
#. Create your working environment
#. Install dependencies
#. Set up project environment variables
#. Run PHX

Install Python 2.7
==================

Windows 7
---------

- Download and install python from http://python.org/download/

- Adjust your PATH environment variable to include paths to Python executable and additional scripts. Add to PATH::

    C:\Python27\;C:\Python27\Scripts;


Set up github
=============

Windows 7, the easy way
-----------------------

- Download github app http://windows.github.com/
- Install and set up/connect to your github account with the installer.


Normal way
----------

To set up github follow the instructions on this page
https://help.github.com/articles/set-up-git

If you already have an github account and git installed, you can skip this step.


Get the code
============

Windows 7
---------
- Go to http://github.com and login
- Go to http://github.com/josven/phx/ and click the "Clone to desktop" button on your right side. This will automagic clone the phx repository on your local machine.

Normal way
----------

Read this guide about how to fork a repository
https://help.github.com/articles/fork-a-repo

Use the https://github.com/josven/phx project instead of the "Spoon-Knife".


Set up database
===============

Windows 7
---------

* Download Installer from http://www.enterprisedb.com/products-services-training/pgdownload#windows
* Install postgres from the installer
* Open up pgAdminIII (should be in your start meny)
* Create a new database for phx

Normal way
----------

We use PostgreSQL in production, and I encourage to also use PostgreSQL
in developent.

For help setting up the database i refer to the PostgreSQL docuentation found
here: http://www.postgresql.org/


Create your working environment
===============================

You have several options in setting up your working environment.  We recommend
using virtualenv to seperate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Windows 7
---------

First you need pip intaller and virtualenv

* Download install script for setup tools::

    https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
    
* Execute script in python, open cmd.exe: Start menu > run > powershell [enter]::

    C:\python path_to_downloaded_script/ez_setup.py
    
* Install python package installer (pip)::

    C:\easy_install pip
    
* Install virtualenv::

    C:\pip install virtualenv

* Create a virtual enviroment for phx::

    C:\any_directory_that_you_want_to_store_your_virtual_enviroments\> virtualenv phx
    
* Activate the env::

    C:\path_to_envs\> phx\Scripts\activate
    
    
* (You can deactivate the enviroment by using the deactive command)::

    (phx) C:\dectivate	


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

Installation of dependencies
=============================

Windows 7
---------

* Open powershell
* Make sure you have the phx enviroment active
* Navigate to your local repository of the phx code (Documents/GitHub/phx/)::

    C:\Users\you\Documents\GitHub\phx> pip install -r requirements/local.txt
    
**Note 1!**

If you experince error message: "Error: Unable to find vcvarsall.bat"
you have to install Visual Studio C++ 2008 Express Edition (http://download.microsoft.com/download/A/5/4/A54BADB6-9C3F-478D-8657-93B3FC9FE62D/vcsetup.exe)
and re-run pip install -r requirements/local.txt

**Note 2!**

Pillow do not support eggs in windows accordning to Pillow documentation. So uninstall Pillow with pip::

    pip uninstall pillow
    
And reinstall Pillow with easy_install::

    easy_install pillow
    

Normal way
----------
   
Depending on where you are installing dependencies:


First make sure that you using your virtual enviroment.

If you are using virtualenvwrapper::

    $ workon phx-dev

Or just if you just using Virtualenv::

    $ . /path_to_enviroment/bin/activate

Then install dependencies::

    $ pip install -r requirements/local.txt


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

Run PHX
=======

- Run this command in project root::
    
    	$ python phx/manage.py runserver 0:8000 --settings=phx.settings.local

