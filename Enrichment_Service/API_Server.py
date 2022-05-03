from http.server import HTTPServer, BaseHTTPRequestHandler 
import cgi, enrichment, json
 

class Server (BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    def do_POST (self):
        if self.path.endswith("/enrich"):
            content_type = cgi.parse_header(self.headers.get('Content-Type'))
            if  content_type[0] != 'application/json':
                self.send_response(400,message="Please make sure to use a suitable entry!")
                self.end_headers()
                return

            length = int(self.headers.get_all('Content-Length')[0])
            RO_Crate = json.loads(self.rfile.read(length))
            #print(RO_Crate,"HEEEEEEEEEEEEEEEEEEEEEEEEEERE")

            rich_RO=enrichment.enrich_RO(RO_Crate)
            self._set_headers()
            self.wfile.write(json.dumps(rich_RO).encode('utf-8'))
            #print(rich_RO)
            return 

    

def run(server_class=HTTPServer, handler_class=Server, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting your http server on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()