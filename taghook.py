import json
from BaseHTTPServer import (HTTPServer,
                            BaseHTTPRequestHandler)
import SocketServer
import os
import subprocess
import tempfile
from shutil import rmtree


PORT = 12001

class HookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        
        # get json string from post
        content_length = int(self.headers['Content-Length'])
        json_string = self.rfile.read(content_length)

        # send ok
        self.send_response(200)

        # parse json
        data = json.loads(json_string)
        
        ref = data['ref']
        repo = data['repository']['url']

        # handle tag
        handle_tag(repository=repo, reference=ref)


def handle_tag(repository, reference):
    
    # get current directory
    current_dirname = os.getcwd()
    # create a temporary directory
    tempdir_name = tempfile.mkdtemp()

    # change to temporary directory
    os.chdir(tempdir_name)
    # pull repository and checkout the reference
    subprocess.call(['git','clone',repository,'-n','.'])
    subprocess.call(['git','checkout',reference])

    if os.path.exists('setup.py'):
        subprocess.call(['python','setup.py','sdist','upload','-r','internal'])

    # change back to current directory
    os.chdir(current_dirname)
    # delete temporary directory
    rmtree(tempdir_name)
    
        
def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HookHandler)
    print("Start Webserver")
    print("Hit CTL-C to shut down the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()

if __name__ == '__main__':
    run_server()
