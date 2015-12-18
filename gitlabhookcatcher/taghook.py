# Copyright 2014 Sebastian Jordan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import SocketServer
import subprocess
import tempfile
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from shutil import rmtree

from hook import HookHandler, JsonParseError
from util import tempDir


class PackageUploader(HookHandler):
    """Request handler to handle the tag web hook

    You need to specify a pypi repository for the hook handler to
    work.  You do that by setting the pypirepo field of the class:
    HookHandler.pypirepo = "yourrepo".

    Notice that the repo name you specify has to appear in the .pypirc
    of the user running server.
    """

    def __get_routing_table__(self):
        """Get the routing table for the hook handler"""
        table = super(PackageUploader, self).__get_routing_table__()
        table['/'] = partial(
            deprecate,
            PackageUploader.handle_package_upload,
            "Posting to the root is deprecated, use '/tag' path instead")
        table['/tag'] = table['/']
        return table

    def handle_package_upload(self, body, params):
        ref = body['ref']
        repo = body['repository']['url']
        self.send_response(200)
        with tempDir():
            handle_tag(repository=repo,
                       reference=ref,
                       pypi=self.pypirepo,
                       python_path=self.python_path)

    pypirepo = None


def deprecate(fun, msg, *args, **kwargs):
    logging.warn(msg)
    return fun(*args, **kwargs)


def handle_tag(repository, reference, pypi, python_path="python"):
    """checkout revs from a git repo and upload a python sdist to pypi"""

    # pull repository and checkout the reference
    subprocess.call(['git', 'clone', '--quiet', repository, '-n', '.'])
    subprocess.call(['git', 'checkout', '--quiet', reference])

    if os.path.exists('setup.py'):
        if pypi is not None:
            subprocess.call([python_path, 'setup.py', '-q', 'sdist', 'upload',
                             '-r', pypi])
        else:
            subprocess.call([python_path, 'setup.py', '-q', 'sdist', 'upload'])
