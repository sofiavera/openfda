import socket
import http.client
import json

PORT = 8090
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)
    drugs = []
    intro = "<ol>" + "\n"
    end = "<\ol>"
    for i in range(len(repos['results'])):
        drugs.append(i)
    with open("drug.html","w") as f:
        f.write(intro)
        for element in drugs:
            f.write("<\t>" + "<li>" + element + "<\li>")
        f.write(end)
    with open("drug.html","r") as f:
        drugs = f.read()

    web_contents = drugs
    web_headers = "HTTP/1.1 200"
    web_headers += "\n" + "Content-Type: text/html"
    web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
    clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
    clientsocket.close()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
hostname = "localhost"


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
try:
    serversocket.bind((hostname, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print ("Waiting for connections at %s %i" % (hostname, PORT))
        (clientsocket, address) = serversocket.accept()
        process_client(clientsocket)

except socket.error as err:
    print(type(err))
