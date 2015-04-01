from os import curdir
from os.path import join as pjoin
import cgi

from http.server import BaseHTTPRequestHandler, HTTPServer

def get_store_path(name):
    return pjoin(curdir, name[1:])

class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(get_store_path(self.path)) as fh:
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(fh.read().encode())

    def do_POST(self):
        print(self.headers)
        length = int(self.headers['content-length'])

        data = self.rfile.read(int(length))

        with open(get_store_path(self.path), 'bw+') as fh:
            fh.write(data)

        response = bytes("This is the response.", "utf-8") #create response
        self.send_response(200) #create header
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)


server = HTTPServer(('', 8081), StoreHandler)
server.serve_forever()
