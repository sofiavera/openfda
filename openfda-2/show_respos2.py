import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repos = json.loads(repos_raw)
for i in range(len(repos['results'])):
    if repos['results'][i]['openfda'] != {}:
        print("The name if the manufacturer is", repos['results'][i]['openfda']['manufacturer_name'])