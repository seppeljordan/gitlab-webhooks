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

    This is a subclass of BaseHTTPRequestHandler.  You can specify IP
    addresse that are allowed to push events to a hookhandler by
    changing allowdHosts property to a list of strings that represent
    all IP addresses that are allow to push events.
    """
    
    allowedHosts = []

    def checkIP(self):
        (host,port) = self.client_address
        if not self.allowedHosts is None:
            if host in self.allowedHosts:
                return True
            else:
                return False
        else:
            return True

    def getJSON(self):
        """get json data from the request body"""

        # get json string from post
        content_length = int(self.headers['Content-Length'])
        json_string = self.rfile.read(content_length)

        try:
            return json.loads(json_string)
        except ValueError:
            return None

        return None
        
