import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000


class OpenFDAClient(self):
    def get_url(first_param, limit):
        conn = http.client.HTTPSConnection("api.fda.gov")
        input = self.path.split("=")
        first_param = input[0]
        limit = input[1]
        url = "/drug/label.json?search=active_ingredient:" + first_param + "=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    with open("search.html", "r") as f:
        message = f.read()
        self.wfile.write(bytes(message, "utf8"))
first_step = OpenFDAClient
first_step.get_url()
