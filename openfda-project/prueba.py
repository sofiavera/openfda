import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000
MAX_OPEN_REQUESTS = 5

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path == "/":
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif self.path == "searchDrug":
            list_url = self.path.strip("searchDrug")
            active_ingredient = list_url[1]
            final_url = "/drug/label.json?search=active_ingredient:" + active_ingredient
            conn.request("GET", final_url, None, headers)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(drugs_raw)
            new_drugs = str(drugs)
            self.wfile.write(bytes(new_drugs, "utf8"))



Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()
do_GET(self)