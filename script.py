import requests
import csv
import sys

# Takes an API key on the command line and retrieves the first form tied to that API key. It then outputs all the answers as a CSV, with an added index
# Created by Liam Workman

def createDictionaryFromTypeformResponse(typeformResponse,questionKeys):
    iterator = 0
    holder = {}
    for response in typeformResponse:
        questionAnswers = {}
        questionAnswers['token'] = response['token']
        questionAnswers['key'] = iterator
        iterator += 1
        for questionID in questionKeys:
            if questionID not in response['answers']:
                questionAnswers[questionID] = 'NaN'
            else:
                questionAnswers[questionID] = response['answers'][questionID]
        holder[response['token']] = questionAnswers
    return holder

def createCSVFromDict(headers,rows):
    with open('./output/answers.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = headers)
        writer.writeheader()

        for row in rows:
            writer.writerow(rows[row])

def retrieveAllFormsFromTypeform(apiKey):

    formIDRequest = requests.request('GET' , 'https://api.typeform.com/v1/forms?key='+apiKey)

    formID = formIDRequest.json()[0]['id']
    formRequest = requests.request('GET' , 'https://api.typeform.com/v1/form/'+formID+'?key='+apiKey)

    return formRequest.json()

# This is where the magic happens

form = retrieveAllFormsFromTypeform(sys.argv[1])

questionIDs = []

for question in form['questions']:
    questionIDs.append(question['id'])

peoplesResponses = createDictionaryFromTypeformResponse(form['responses'],questionIDs)

createCSVFromDict(['key','token']+questionIDs,peoplesResponses)