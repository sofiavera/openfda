import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000


class OpenFDAClient():
    def get_url(self, first_param, limit):
        url = "/drug/label.json?search=active_ingredient:" + first_param + "=" + limit
        conn.request("GET", url, None, headers)

class OpenFDAParser():
    def get_data(self, path):
        list = []
        for i in range(len(drugs['results'])):
            if path1 == '':
                list.append(drugs['results'][i]['openfda'][path][0])
            else:
                list.append(drugs['results'][i]['openfda'][path][path1][0])

class OpenFDAHTML():
    def write_data(self):
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

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        with open("search.html", "r") as f:
            message = f.read()
            self.wfile.write(bytes(message, "utf8"))
            headers = {'User-Agent': 'http-client'}
            if self.path != '/':
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                first_param = input[0]
                limit = input[1]
                OpenFDAClient.get_url()
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                if "searchDrug" in self.path:
                    path = 'active_ingredient'
                    path1 = ''
                elif "searchCompany" in self.path:
                    path = 'openfda'
                    path1 = 'manufacturer_name'
                OpenFDAParser().get_data()
                OpenFDAHTML().write_data()

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
do_GET(self)

