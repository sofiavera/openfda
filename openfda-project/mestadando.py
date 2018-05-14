import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True
IP = "localhost"
PORT = 8000


class OpenFDAClient():
    def url_search(self, choice, first_param, limit ):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")

        url = "/drug/label.json?search" + choice + first_param + "&limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        search_raw = r1.read().decode("utf-8")
        conn.close()

        search = json.loads(search_raw)
        return search


    def lists(self, limit):
        query = "limit=" + limit
        lists = self.get_url(query)
        return lists

class OpenFDAParser():
    def parser_search(self, search, path, path1):
        list = []
        try:
            for i in range(len(search['results'])):
                if path1 == '':
                    list.append(search['results'][i]['openfda'][path][0])
                else:
                    list.append(search['results'][i]['openfda'][path][path1][0])
        except KeyError:
            list.append("unknown")

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

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if path == "/":
            with open("search.html", "r") as f:
                message = f.read()
                self.wfile.write(bytes(message, "utf8"))
        elif 'search' in path:
            first_param = path.split("=")[1].split("&")[0]
            if "Drug" in path:
                choice = "active_ingredient:"
                path = 'active_ingredient'
                path1 = ''
            else:
                choice = "manufacturer_name:"
                path = 'openfda'
                path1 = 'manufacturer_name'
            if '&' in path:
                limit = path.split("=")[2]
            else:
                limit = '10'
            search = client.url_search(choice, first_param, limit)
            list = parser.parser_search(path,search, path, path1)
            contents = HTML.write_data(self, list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listDrugs' in path:
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
            else:
                limit = '10'
            info = client.list_drugs(limit)
            drugs_list = parser.parser_drugs(self, info)
            contents = HTML.write_data(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listCompanies' in path:
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
            else:
                limit = '10'
            info = client.list_drugs(limit)
            drugs_list = parser.parser_company(self, info)
            contents = HTML.write_data(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
do_GET()