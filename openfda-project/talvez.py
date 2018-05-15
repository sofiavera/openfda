import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True
IP = "localhost"
PORT = 8000

class OpenFDAClient():
    def url_drugs(self, active_ingredient, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?" + "search=active_ingredient:" + active_ingredient + "&limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        search = json.loads(drugs_raw)
        return search
    def url_companies(self, manufacturer_name, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?" + "search=active_ingredient:" + manufacturer_name + "&limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        search = json.loads(drugs_raw)
        return search
    def url_lists(self, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        lists = json.loads(drugs_raw)
        return lists
class OpenFDAParser():
    def data_drugs(self, search):
        list = []
        try:
            for i in range(len(search['results'])):
                list.append(search['results'][i]['active_ingredient'][0])
        except KeyError:
            list.append("Unknown")
        return list
    def data_companies(self, search):
        list = []
        try:
            for i in range(len(drugs['results'])):
                list.append(drugs['results'][i]['openfda']['manufacturer_name'][0])
        except KeyError:
            list.append("Unknown")
        return list
    def data_warnings(self,lists):
        try:
            for i in range(len(drugs['results'])):
                list.append(drugs['results'][i]['warnings'][0])
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
        parser = OpenFDAParser
        HTML = OpenFDAHTML

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

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if path == "/":
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif "searchDrug" in path:
            print("kk")
            input = self.path.split("=")
            active_ingredient = input[1].split("&")[0]
            if "limit" not in path or input[2]=='':
                limit = '10'
            else:
                limit = input[2]
            search = client.url_drugs(active_ingredient, limit)
            list = parser.data_drugs(search)
            final = HTML.write_data(list)
            self.wfile.write(bytes(final, "utf8"))
        elif "searchCompany" in path:
            input = self.path.split("=")
            manufacturer_name = input[1].split("&")[0]
            if input[2]=='':
                limit = '10'
            else:
                limit = input[2]
            search = client.url_companies(manufacturer_name, limit)
            list = parser.data_companies(search)
            final = HTML.write_data(list)
            self.wfile.write(bytes(final, "utf8"))
        elif "listDrugs" in path:
            input = self.path.split("=")
            if input[2] == '':
                limit = '10'
            else:
                limit = input[2]
            lists = client.url_lists(limit)
            list = parser.data_drugs(lists)
            final = HTML.write_data(list)
            self.wfile.write(bytes(final, "utf8"))
        elif "listCompanies" in path:
            input = self.path.split("=")
            if "limit" not in path or input[2] == '':
                limit = '10'
            else:
                limit = input[2]
            lists = client.url_lists(limit)
            list = parser.data_companies(lists)
            final = HTML.write_data(list)
            self.wfile.write(bytes(final, "utf8"))
        elif "listWarnings" in path:
            input = self.path.split("=")
            if "limit" not in path or input[2] == '':
                limit = '10'
            else:
                limit = input[2]
            lists = client.url_lists(limit)
            list = parser.data_warnings(lists)
            final = HTML.write_data(list)
            self.wfile.write(bytes(final, "utf8"))
        elif 'secret' in path:
            status_code = 401
            print('Status code:' + str(status_code))
        elif 'redirect' in path:
            status_code = 302
            print('Status code:' + str(status_code))
        else:
            status_code = 404
            print('Status code:' + str(status_code))
            with open("not_found.html") as f:
                message = f.read()
            self.wfile.write(bytes(message, "utf8"))

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
do_GET()