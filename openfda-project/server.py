import http.server
import socketserver
import http.client
import json

IP = "localhost"
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

class OpenFDAClient():
    def get_url(self,choice,first_param, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")

        if choice != '':
            url = "/drug/label.json?search=" + choice + ':' + first_param + '&limit=' + limit
        else:
            url = "/drug/label.json?limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        search = json.loads(drugs_raw)

        return search

class OpenFDAParser():
    def parser(self, choice, search):

        list = []
        for i in range(len(search['results'])):
            if choice == 'active_ingredient'or  choice == 'warnings':
                try:
                    list.append(search['results'][i][choice][0])
                except KeyError:
                    list.append("Unknown")
            elif choice == 'manufacturer_name':
                try:
                    list.append(search['results'][i]['openfda'][choice][0])
                except KeyError:
                    list.append("Unknown")

        return list
class OpenFDAHTML():
    def write_data(self, list):
        intro = "<!doctype html>" + "<html>" + "<body>" + "<ul>"
        end = "</ul>" + "</body>" + "</html>"

        with open("empty.html", 'w') as f:
            f.write(intro)
            for element in list:
                f.write("<li>" + element + "</li>")
            f.write(end)

        with open('empty.html', 'r') as f:
            file = f.read()
        return file

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client = OpenFDAClient()
        parser = OpenFDAParser()
        HTML = OpenFDAHTML()
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                with open("search.html", "r") as f:
                    menu = f.read()
                    self.wfile.write(bytes(menu, "utf8"))

            elif 'search' in self.path or 'list' in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                if 'searchDrug' in self.path:
                    choice = "active_ingredient"
                elif 'searchCompany' in self.path:
                    choice = "manufacturer_name"
                else:
                    choice = ''

                input = self.path.split("=")
                first_param = self.path.split("=")[1].split("&")[0]
                if "&" in input[1]:
                    if input[2] == '':
                        limit = '10'
                    else:
                        limit = input[2]
                else:
                    limit = '10'

                search = client.get_url(choice, first_param, limit)

                if choice == '':
                    if 'Drugs' in self.path:
                        choice = 'active_ingredient'
                    elif 'Companies' in self.path:
                        choice = 'manufacturer_name'
                    elif 'Warnings' in self.path:
                        choice = 'warnings'

                list = parser.parser(choice, search)

                file = HTML.write_data(list)

                self.wfile.write(bytes(file, "utf8"))

            elif "secret" in self.path:
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic Realm = "OpenFDA Private Zone"')
                self.end_headers()

            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header('Location', 'http://localhost:8000/')
                self.end_headers()

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open("error.html", "r") as f:
                    file = f.read()
                self.wfile.write(bytes(file, "utf8"))

        except KeyError as ex:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("error.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))

        return

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
