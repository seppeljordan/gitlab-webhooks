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

from BaseHTTPServer import BaseHTTPRequestHandler
import json

class HookHandler(BaseHTTPRequestHandler):
    """Handler for gitlab webhooks

    This is a subclass of BaseHTTPRequestHandler.  

    You can specify IP addresse that are allowed to push events to a
    hookhandler by changing allowdHosts property to a list of strings
    that represent all IP addresses that are allow to push events.

    You can enable a check for valid repository locations by setting
    the allowedRepos property of the class to a list of domains that
    are accepted by the hook, e.g. ["scm.company.net",
    "git.scm.company.net"].

    You can specify the python interpreter that is used to make the
    distribution by changing the class property `python_path` to the
    desired path, e.g. `HookHandler.python_path = "/usr/bin/python3".
    """
    
    allowedHosts = None
    allowedRepos = None
    python_path = "python"

    def checkIP(self):
        """Check if a request came from an allowed ip address"""
        (host,port) = self.client_address
        if self.allowedHosts is None or \
           self.allowedHosts == []:
            return True
        else:
            if host in self.allowedHosts:
                return True
            else:
                return False

    def getJSON(self):
        """get json data from the request body"""

        # get json string from post
        content_length = int(self.headers['Content-Length'])
        json_string = self.rfile.read(content_length)

        try:
            # return json
            return json.loads(json_string)
        except ValueError:
            # json was invalid
            return None
        return None
        
    def checkRepoURL(self,address):
        """Check if the repository address is valid and allowed"""

        if self.allowedRepos is None:
            return True
        
        hostname = address.partition("@")[2].partition(":")[0]

        if hostname in self.allowedRepos:
            return True
        else:
            return False
