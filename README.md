Introduction
============

This package implements a simple catcher for gitlab tag event webhooks.
The program will checkout the tag, create a source distribution of the
python package and upload it to a given pypi. There is also a helper
script to upload existing tags in a repository to pypi.

Usage
=====

gitlab-taghook-upload-tags
--------------------------

This script clones a repository to a temporary folder and pushes all
tags as source releases to a specified pypi repository.

Arguments:

-   `--pypi PYPINAME` PyPI repository where to upload your
    product to
-   `--repository REPO` URL pointing to the git repository
    of your sources
-   `--python-path PATH` optional argument, path to the
    python interpreter used to create the distribution

gitlab-taghook-catcher
----------------------

When calling the catcher with `gitlab-taghook-catcher` you
have to give two arguments.

-   `--port PORT` specifies the port (surprise)
-   `--repository REPO` specifies the name of the pypi
    where to upload to
-   `--allowed IP [IP ...]` optional argument, list of
    hosts that are allowed to push events to the server
-   `--gitlabdomain DOMAIN [DOMAIN ..]` optional argument,
    list of hostnames of authorized gitlab instances
-   `--python-path PATH` optional argument, path to the
    python interpreter used to create the distribution

The taghook catcher is currently only capable of on type of action and
that is publishing a python package onto a specified pypi server. To use
this functionality you have to send your post requests to
`hookcatcher.domain/tag`, where
`hookcatcher.domain` is the address of your hook catcher
instance and `/tag` is the path that triggers the package
building functionality. You can also post to the root path but this is
deprecated.

usage in gitlab
---------------

To use this program for a specific gitlab repository, go to the settings
section of the repository. Select the trigger you want to configure,
e.g. "Tag push events" if you want to send a request to the hook catcher
when somebody pushes a tag to your gitlab repository. Then enter the url
pointing to the hook catcher. Pay attention to the path, see section
"Usage -&gt; gitlab-taghook-catcher".

Configuration
=============

For the script to work it is requiered that user who executes the script
has a properly configured `.pypirc`. Also the user running
script needs read access to the gitlab repository to checkout the
source.

License and Copyright
=====================

Copyright 2014 Sebastian Jordan

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see &lt;<http://www.gnu.org/licenses/>&gt;.
