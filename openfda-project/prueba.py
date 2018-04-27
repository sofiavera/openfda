import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if "/" == self.path:
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif "searchDrug" in self.path:
            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            input = self.path.split("=")
            url =  "/drug/label.json?search=active_ingredient:" + input[1]
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()
            drugs = json.loads(drugs_raw)
            list = []
            for i in range(len(drugs['results'])):
                list.append(drugs['results'][i]['id'])
            print(len(list))
            intro = "<!doctype html>" + "<html>" + "<body>" + "<ul>"
            end = "</ul>" + "</body>" + "</html>"
            with open("empty.html", 'w') as f:
                f.write(intro)
                for element in list:
                    f.write("<li>" + element + "</li>")
                f.write(end)
            with open('empty.html', 'r') as f:
                file = f.read()
                self.wfile.write(bytes(file, "utf8"))

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass
httpd.server_close()
do_GET(self)