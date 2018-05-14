import http.server
import socketserver
import http.client
import json

socketserver.TCPServer.allow_reuse_address = True
IP = "localhost"
PORT = 8000


class OpenFDAClient():
    def search_drugs(self, active_ingredient, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?" + "search=active_ingredient:" + active_ingredient + "&limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        search_drugs = json.loads(drugs_raw)
        return search_drugs

    def search_companies(self, manufacturer_name , limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?" + "search=active_ingredient:" + manufacturer_name + "&limit=" + limit
        conn.request("GET", url, None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        search_companies = json.loads(drugs_raw)
        return search_companies

    def lists(self, limit):
        query = "limit=" + limit
        lists = self.get_url(query)
        return lists

class OpenFDAParser():
    def parser_drugs(self, drugs):
        list = []
        try:
            for i in range(len(drugs['results'])):
                list.append(drugs['results'][i]['active_ingredient'][0])
        except KeyError:
            list.append("Unknown")
        return list

    def parser_company(self, search_companies):
        list = []
        try:
            for i in range(len(search_companies['results'])):
                list.append(search_companies['results'][i]['openfda']['manufacturer_name'][0])
        except KeyError:
            list.append("unknown")

        return list

    def parse_warnings(self, info):

        warning_list = []

        for i in range(len(info['results'])):
            try:
                if "warnings" in info["results"][i]:
                    warning_list.append(info['results'][i]['warnings'][0])
                else:
                    warning_list.append("Unknown")
            except KeyError:
                warning_list.append("Unknown")
                continue

        return warning_list


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
        elif 'searchDrug' in self.path:
            print("kk")
            input = path.split("=")
            if path.split("=")[2] == '':
                limit = '10'
            else:
                limit = path.split("=")[2]
            search_drugs = client.search_drugs(active_ingredient, limit)
            drugs_list = parser.parser_drugs(search_drugs)
            contents = HTML.write_data(drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'searchCompany' in path:
            manufacturer_name = path.split("=")[1].split("&")[0]
            if 'limit' in path:
                limit = path.split("=")[2]
            else:
                limit = '10'
            search_company = client.search_companies(manufacturer_name, limit)
            company_list = parser.parser_company(search_company)
            contents = HTML.write_data (company_list)
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

        elif 'listCompanies' in path:
            print('Client request: listCompanies')
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.list_drugs(limit)
            drugs_list = parser.parse_companies(self, info)
            contents = html.build_html(self, drugs_list)
            self.wfile.write(bytes(contents, "utf8"))

        elif 'listWarnings' in path:
            print('Client request: listWarnings')
            if 'limit' in path:
                limit = path.split("=")[1].split("&")[0]
                if limit == '':
                    limit = 10
            else:
                limit = '10'
            info = client.list_drugs(limit)
            warning_list = parser.parse_warnings(self, info)
            contents = html.build_html(self, warning_list)
            self.wfile.write(bytes(contents, "utf8"))

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