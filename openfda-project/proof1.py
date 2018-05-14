import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True
IP = "localhost"
PORT = 8000

class OpenFDAClient():

    def url_search(self, choice, first_param, limit):

        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")

        url = "/drug/label.json/search=" + choice + first_param + "&limit=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()  ñ
        drugs = json.loads(drugs_raw)


class OpenFDAParser():
    def get_data(self, drugs):

        list = []
        for i in range(len(drugs['results'])):
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

        client = OpenFDAClient()
        parser = OpenFDAParser()
        html = OpenFDAHTML()

        path = self.path


        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            status_code = 200
        elif 'secret' in path:
            status_code = 401
        elif 'redirect' in path:
            status_code = 302
        else:
            status_code = 404


        self.send_response(status_code)

        if path == "/" or 'searchDrug' in path or 'searchCompany' in path or 'listDrugs' in path or 'listCompanies' in path or 'listWarnings' in path:
            self.send_header('Content-type', 'text/html')
        elif 'secret' in path:
            self.send_header('WWW-Authenticate', 'Basic realm="OpenFDA Private Zone"')
        elif 'redirect' in path:
            self.send_header('Location', 'http://localhost:8000/')

        self.send_header('Content-type', 'text/html')
        self.end_headers()



        if path == "/":
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif 'search'in self.path:
            if 'Drug' in self.path:
                choice = "active_ingredient:"
            else:
                choice = "manufacturer_name:"
            if "&" in self.path:
                first_param = self.path.split("=")[1].split("&")[0]
                limit = self.path.split("=")[2]
            else:
                first_param = self.path.split("=")[1]
                limit = 10
            drugs = client.url_search(self, choice, first_param, limit)
            if "searchDrug" in self.path:
                path = 'active_ingredient'
                path1 = ''
            elif "searchCompany" in self.path:
                path = 'openfda'
                path1 = 'manufacturer_name'
            parser = parser.get_data(self, drugs, path)
            contents = html.write_data(self, parser)
            self.wfile.write(bytes(contents, "utf8"))

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
do_GET()
httpd.server_close()

