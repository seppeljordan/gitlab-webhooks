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
import logging
from urlparse import urlparse, parse_qs
from os.path import normpath

class JsonParseError(Exception):
    pass

class RoutingError(Exception):
    pass

class HookHandler(BaseHTTPRequestHandler,object):
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

    This class is meant for subclassing.  You can implement your
    functionality by inheriting from this class.  Then you have to
    implement a function that takes the request content (JSON) and the
    request parameter as a dictionary.  The implementer of this
    funcionality has to send the correct response.  See
    'gitlabhookcatcher.taghook.PackageUploader' for an example.
    """

    allowedHosts = None
    allowedRepos = None
    python_path = "python"
    routing_table = {}

    def __get_routing_table__(self):
        return {}
    
    def check_ip(self, host):
        """Check if a request came from an allowed ip address"""
        if self.allowedHosts is None or \
           self.allowedHosts == []:
            return True
        else:
            if host in self.allowedHosts:
                return True
            else:
                return False

    def get_json(self):
        """get json data from the request body"""

        # get json string from post
        content_length = int(self.headers['Content-Length'])
        json_string = self.rfile.read(content_length)

        try:
            # return json
            return json.loads(json_string)
        except ValueError:
            raise JsonParseError("The content of the post request was not "
                                 "valid json")

    def send_response(self,code):
        ret = super(HookHandler,self).send_response(code)
        client_addr, _ = self.client_address
        logging.info('Sent reply, "%s", "%s"' % (client_addr,str(code)))
        return ret        
        
    def check_repo_url(self,address):
        """Check if the repository address is valid and allowed"""

        if self.allowedRepos is None:
            return True
        
        hostname = address.partition("@")[2].partition(":")[0]

        if hostname in self.allowedRepos:
            return True
        else:
            return False

    def do_POST(self):
        self.handle_post_path()
        
    def handle_post_path(self):
        client_addr, _ = self.client_address
        if not self.check_ip(client_addr):
            logging.info('Client address not allowed, %s',
                         client_addr)
            self.send_response(403)
            return None
        try:
            content = self.get_json()
        except JsonParseError:
            logging.info('Invalid JSON, "%s"', client_addr)
            self.send_response(400)
            return None
        repo = content['repository']['url']
        if not self.check_repo_url(repo):
            logging.info('Repository not allowed: "%s", %s',
                         repo, client_addr)
            self.send_response(403)
            return None
        path = urlparse(self.path)
        get_params = parse_qs(path.query)
        post_path = normpath(path.path)
        routes = self.__get_routing_table__()
        try:
            routes[post_path](self,
                              body=content,
                              params=get_params)
        except KeyError:
            raise RoutingError('Cannot find "%s" in routing table' % post_path)
