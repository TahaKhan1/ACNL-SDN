import json 
import requests
### Example of RYU Book###
##===========Set the interface Addresses=============
# ======================s1===========================
url = 'http://localhost:8080/router/0000000000000001'
payload = {'address':'172.16.20.1/24'}
r = requests.post(url, data=json.dumps(payload))

url = 'http://localhost:8080/router/0000000000000001'
payload = {'address': '172.16.30.30/24'}
r = requests.post(url, data=json.dumps(payload))
print (r.status_code)

  # =======================s2==========================
url = 'http://localhost:8080/router/0000000000000002'
payload = {'address': '172.16.10.1/24'}
r = requests.post(url, data=json.dumps(payload))

url = 'http://localhost:8080/router/0000000000000002'
payload = {'address': '172.16.30.1/24'}
r = requests.post(url, data=json.dumps(payload))

url = 'http://localhost:8080/router/0000000000000002'
payload = {'address': '192.168.10.1/24'}
r = requests.post(url, data=json.dumps(payload))
print (r.status_code)

  # =======================s3==========================
url = 'http://localhost:8080/router/0000000000000003'
payload = {'address': '192.168.30.1/24'}
r = requests.post(url, data=json.dumps(payload))

url = 'http://localhost:8080/router/0000000000000003'
payload = {'address': '192.168.10.20/24'}
r = requests.post(url, data=json.dumps(payload))
print (r.status_code)
