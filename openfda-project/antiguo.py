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
        try:
            if "/" == self.path:
                with open("search.html", "r") as f:
                    message = f.read()
                    self.wfile.write(bytes(message, "utf8"))
            elif "searchDrug" in self.path:
                print(self.path)
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                url = "/drug/label.json?search=active_ingredient:" + input[1] + "=" + input[2]
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                list = []
                for i in range(len(drugs['results'])):
                    list.append(drugs['results'][i]['active_ingredient'][0])
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
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                url ="/drug/label.json?search=manufacturer_name:" + input[1] + "=" + input[2]
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                list = []
                for i in range(len(drugs['results'])):
                    list.append(drugs['results'][i]['openfda']['manufacturer_name'][0])
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
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                url ="/drug/label.json?" + "limit=" + input[1]
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                list = []
                for i in range(len(drugs['results'])):
                    if 'brand_name' in drugs['results'][i]['openfda']:
                        list.append(drugs['results'][i]['openfda']['brand_name'][0])
                    else:
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
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                url ="/drug/label.json?" + "limit=" + input[1]
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                list = []
                for i in range(len(drugs['results'])):
                    if 'manufacturer_name' in drugs['results'][i]['openfda']:
                        list.append(drugs['results'][i]['openfda']['manufacturer_name'][0])
                    else:
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
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                input = self.path.split("=")
                url ="/drug/label.json?" + "limit=" + input[1]
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drugs = json.loads(drugs_raw)
                list = []
                for i in range(len(drugs['results'])):
                    if 'warnings' in drugs['results'][i]:
                        list.append(drugs['results'][i]['warnings'][0])
                    else:
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
        except:
            with open('error.html','w') as f:
                f.write("<!doctype html>" + "<html>" + "<body>" + "<h1>" + "ERROR 404, NOT FOUND"+"</h1>"+"</body>" + "</html>")
            with open('error.html', 'r') as f:
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