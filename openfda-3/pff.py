import http.server
import socketserver
import json
import http.client

IP = "localhost"
PORT = 8000
MAX_OPEN_REQUESTS = 5

class manzana(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=10", None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()

        repos = json.loads(repos_raw)
        drugs = []
        for i in range(len(repos['results'])):
            print(i)
            try:
                drugs.append(repos['results'][i]['active_ingredient'][0])
            except KeyError:
                drugs.append("This index has no drug")
        with open("drug.html", "w") as f:
            for elem in drugs:
                f.write("<li>" + elem )
        with open("drug.html", "r") as f:
            drugs = f.read()
        drugs=drugs+ self.path
        self.wfile.write(bytes(drugs, "utf8"))




Handler = manzana

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()
do_GET(self)