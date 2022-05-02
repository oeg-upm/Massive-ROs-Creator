import requests, json

#!curl -d 'client_id=rohub2020-frontend-devel' -d 'client_secret=194613be-6279-43ac-9b7b-b9959f28da27' -d 'username=george_hadib' -d 'password=George123#' -d 'grant_type=password' 'https://sso.apps.paas-dev.psnc.pl/auth/realms/rohub/protocol/openid-connect/token' | python -m json.tool
#!curl -d 'client_id=rohub2020-frontend-devel' -d 'client_secret=194613be-6279-43ac-9b7b-b9959f28da27' -d 'username=oso_peligroso' -d 'password=oso_peligroso' -d 'grant_type=password' 'https://sso.apps.paas-dev.psnc.pl/auth/realms/rohub/protocol/openid-connect/token' | python -m json.tool

data1 = {
  'client_id': 'rohub2020-frontend-devel',
  'client_secret': '194613be-6279-43ac-9b7b-b9959f28da27',
  'username': 'oso_peligroso',
  'password': 'oso_peligroso',
  'grant_type': 'password'
}
data = {
  'client_id': 'rohub2020-frontend-devel',
  'client_secret': '194613be-6279-43ac-9b7b-b9959f28da27',
  'username': 'george_hadib',
  'password': 'George123#',
  'grant_type': 'password'
}

response = requests.post('http://localhost:8008', data=data)

print (response)