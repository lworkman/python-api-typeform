import requests
apiKey = 'ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d'

formIDRequest = requests.request('GET' , 'https://api.typeform.com/v1/forms?key='+apiKey)
formID = formIDRequest.json()[0]['id']

print(formID)

formRequest = requests.request('GET' , 'https://api.typeform.com/v1/form/'+formID+'?key='+apiKey)