import http.server
import socketserver
import http.client
import json

IP = 'localhost'
PORT = 8000
with open("search.html", "r") as f:
    message = f.read()
    self.wfile.write(bytes(message, "utf8"))
class OpenFDAClient(self, first_param, limit):
    conn = http.client.HTTPSConnection("api.fda.gov")
    input = self.path.split("=")
    first_param = input[0]
    limit = input[1]
    def get_url (first_param,limit):
        url = "/drug/label.json?search=active_ingredient:" + first_param + "=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
get_url()
