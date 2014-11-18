.. contents::

Introduction
============

This package implements a simple catcher for gitlab tag event
webhooks.  The program will checkout the tag, create a source
distribution of the python package and upload it to a given pypi.

Usage
=====

When calling the catcher with `gitlab-taghook-catcher` you have to give
two arguments.

* :code:`--port PORT` specifies the port (suprise)
* :code:`--repository REPO` specifies the name of the pypi where to
  upload to

Configuration
=============

For the script to work it is requiered that user who executes the
script has a properly configured :code:`.pypirc`.  Also the user
running script needs read access to the gitlab repository to checkout
the source.
