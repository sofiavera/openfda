import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000


class OpenFDAClient():
    def url_search(self, first_param, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?search=" + first_param + "=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        drugs = json.loads(drugs_raw)

class OpenFDAParser():
    def get_data(self, drugs, path):
        list = []
        try:
            for i in range(len(drugs['results'])):
                if path1 == '':
                    list.append(drugs['results'][i]['openfda'][path][0])
                else:
                    list.append(drugs['results'][i]['openfda'][path][path1][0])
        except KeyError:
            list.append("unknown")

class OpenFDAHTML():
    def write_data(self, parser):
        intro = "<!doctype html>" + "<html>" + "<body>" + "<ul>"
        end = "</ul>" + "</body>" + "</html>"
        with open("empty.html", 'w') as f:
            f.write(intro)
            for element in parser:
                f.write("<li>" + element + "</li>")
            f.write(end)
        with open('empty.html', 'r') as f:
            file = f.read()


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        client = OpenFDAClient()
        parser = OpenFDAParser()
        HTML = OpenFDAHTML()

        if self.path == "/":
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif "search" in self.path:
            if "&" in self.path:
                first_param = self.path.split("=")[1].split("&")[0]
                limit = self.path.split("=")[2]
            else:
                first_param = self.path.split("=")[1]
                limit = 10
            drugs = client.url_search(first_param, limit)
            if "searchDrug" in self.path:
                path = 'active_ingredient'
                path1 = ''
            elif "searchCompany" in self.path:
                path = 'openfda'
                path1 = 'manufacturer_name'
            parser = parser.get_data(drugs, path)
            file = HTML.write_data(parser)
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

