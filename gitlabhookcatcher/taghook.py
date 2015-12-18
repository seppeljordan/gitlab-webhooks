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
import subprocess
from functools import partial
from shutil import rmtree

from hook import HookHandler, JsonParseError
from util import tempDir


class PackageBuildError(Exception):
    def __init__(self, *args, **kwargs):
        try:
            build_stdout = kwargs['build_stdout']
            del kwargs['build_stdout']
        except KeyError:
            build_stdout = None
        try:
            build_stderr = kwargs['build_stderr']
            del kwargs['build_stderr']
        except KeyError:
            build_stderr = None
        ret = super(PackageBuildError, self).__init__(*args, **kwargs)
        self.stdout = build_stdout
        self.stderr = build_stderr
        return ret


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
        table['/tag'] = PackageUploader.handle_package_upload
        return table

    def handle_package_upload(self, body, params):
        ref = body['ref']
        repo = body['repository']['url']
        with tempDir():
            try:
                handle_tag(repository=repo,
                           reference=ref,
                           pypi=self.pypirepo,
                           python_path=self.python_path)
            except PackageBuildError as e:
                logging.error('Package from repository "%s", reference "%s", '
                              'cannot be build', repo, ref)
                if e.stdout:
                    logging.error('stdout of build command\n' + e.stdout)
                if e.stderr:
                    logging.error('stderr of build command\n' + e.stderr)
                self.send_response(400)
                return
        self.send_response(200)

    pypirepo = None


def deprecate(fun, msg, *args, **kwargs):
    logging.warn(msg)
    return fun(*args, **kwargs)


def handle_tag(repository, reference, pypi, python_path="python"):
    """checkout revs from a git repo and upload a python sdist to pypi"""

    # pull repository and checkout the reference
    subprocess.call(['git', 'clone', '--quiet', repository, '-n', '.'])
    subprocess.call(['git', 'checkout', '--quiet', reference])

    cmd = [python_path, 'setup.py', '-q', 'sdist', 'upload']
    if pypi is not None:
        cmd += ['-r', pypi]

    if not os.path.exists('setup.py'):
        raise PackageBuildError('setup.py was not found in repository "%s" '
                                'for reference "%s"' % (repository, reference))
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    if proc.returncode != 0:
        raise PackageBuildError('Cannot build package from repository "%s", '
                                'reference "%s"' % (repository, reference),
                                build_stdout=proc_out,
                                build_stderr=proc_err)
