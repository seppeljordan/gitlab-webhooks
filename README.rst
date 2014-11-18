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

* `--port PORT` specifies the port (suprise)
* `--repository REPO` specifies the name of the pypi where to upload
  to
