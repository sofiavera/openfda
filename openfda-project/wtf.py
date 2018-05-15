import http.server
import socketserver
import http.client
import json

IP = "localhost"
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open("search.html", "r") as f:
                    menu = f.read()
                    self.wfile.write(bytes(menu, "utf8"))
            elif "searchDrug" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                input = self.path.split("=")
                active_ingredient = self.path.split("=")[1].split("&")[0]
                if "&" in input[1]:
                    if input[2] == '':
                        limit = '10'
                    else:
                        limit = input[2]
                else:
                    limit = '10'

                url = "/drug/label.json?search=active_ingredient:" + active_ingredient + '&limit=' + limit
                print('You take the info from', url)
                conn.request("GET", url, None, headers)

                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

                search = json.loads(drugs_raw)

                list=[]
                for i in range(len(search['results'])):
                    try:
                        list.append(search['results'][i]['active_ingredient'][0])
                    except KeyError:
                        list.append("Unknown")

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
            elif "searchCompany" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                input = self.path.split("=")
                manufacturer_name = self.path.split("=")[1].split("&")[0]
                if "&" in input[1]:
                    if input[2] == '':
                        limit = '10'
                    else:
                        limit = input[2]
                else:
                    limit = '10'

                url = "/drug/label.json?search=manufacturer_name:" + manufacturer_name + '&limit=' + limit
                print('You take the info from', url)
                conn.request("GET", url, None, headers)

                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

                search = json.loads(drugs_raw)

                list=[]
                try:
                    for i in range(len(search['results'])):
                        list.append(search['results'][i]['openfda']['manufacturer_name'][0])
                except KeyError:
                    list.append("Unknown")

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
            elif "listDrugs" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                input = self.path.split("=")
                print(self.path)
                if "limit" in input[0]:
                    if input[1] == '':
                        limit = '10'
                    else:
                        limit = input[1]
                else:
                    limit = '10'

                url = "/drug/label.json?&limit=" + limit
                print('You take the info from', url)
                conn.request("GET", url, None, headers)

                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

                search = json.loads(drugs_raw)

                list=[]
                for i in range(len(search['results'])):
                    try:
                        list.append(search['results'][i]['active_ingredient'][0])
                    except KeyError:
                        list.append("Unknown")

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
            elif "listCompanies" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                input = self.path.split("=")

                if "limit" in input[0]:
                    if input[1] == '':
                        limit = '10'
                    else:
                        limit = input[1]
                else:
                    limit = '10'

                url = "/drug/label.json?limit=" + limit
                print('You take the info from', url)
                conn.request("GET", url, None, headers)

                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

                search = json.loads(drugs_raw)

                list=[]
                for i in range(len(search['results'])):
                    try:
                        list.append(search['results'][i]['openfda']['manufacturer_name'][0])
                    except KeyError:
                        list.append("Unknown")


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
            elif "listWarnings" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")

                input = self.path.split("=")
                if "limit" in input[0]:
                    if input[1] == '':
                        limit = '10'
                    else:
                        limit = input[1]
                else:
                    limit = '10'

                url = "/drug/label.json?limit=" + limit
                print('You take the info from', url)
                conn.request("GET", url, None, headers)

                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

                search = json.loads(drugs_raw)

                list=[]
                try:
                    for i in range(len(search['results'])):
                        list.append(search['results'][i]['warnings'][0])
                except KeyError:
                    list.append("Unknown")

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


