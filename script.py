import requests
import csv
apiKey = 'ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d'

formIDRequest = requests.request('GET' , 'https://api.typeform.com/v1/forms?key='+apiKey)
formID = formIDRequest.json()[0]['id']

formRequest = requests.request('GET' , 'https://api.typeform.com/v1/form/'+formID+'?key='+apiKey)

questionIDs = []

for question in formRequest.json()['questions']:
    questionIDs.append(question['id'])

print(len(formRequest.json()['responses']))

peoplesResponses = {}

iterator = 0

for response in formRequest.json()['responses']:
    questionAnswers = {}
    questionAnswers['token'] = response['token']
    questionAnswers['key'] = iterator
    iterator += 1
    for questionID in questionIDs:
        if questionID not in response['answers']:
            questionAnswers[questionID] = float('NaN')
        else:
            questionAnswers[questionID] = response['answers'][questionID]
    peoplesResponses[response['token']] = questionAnswers

# for response in peoplesResponses:
#     print(peoplesResponses[response])

with open('./output/answers.csv','w') as csvfile:
    fieldnames = ['key','token'] + questionIDs
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()

    for people in peoplesResponses:
        writer.writerow(peoplesResponses[people])