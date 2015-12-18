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

import os
import tempfile
from contextlib import contextmanager
from shutil import rmtree


@contextmanager
def tempDir():
    """Execute fun with cwd pointing to a new temporal directory.

    cwd means current working directory.
    """
    current = os.getcwd()
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

    yield tmpdir

    os.chdir(current)
    rmtree(tmpdir)
