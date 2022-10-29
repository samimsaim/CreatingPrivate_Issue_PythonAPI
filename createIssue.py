from sqlite3 import DatabaseError
import requests
import json

data = {
    'token': 'token here',
    'content': 'record',
    'action': 'export',
    'format': 'json',
    'type': 'flat',
    'csvDelimiter': '',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'exportSurveyFields': 'false',
    'exportDataAccessGroups': 'false',
    'returnFormat': 'json',
    'dateRangeBegin': '2022-08-07 00:00:00',
    'dateRangeEnd': '2022-08-07 23:59:59'
}

r = requests.post('https://showmeportal.missouri.edu/redcap/api/', data=data)
print('HTTP Status: ' + str(r.status_code))
my_dict = r.json()

# print(my_dict)
# These codes remain the same
username = "samimsaim"
Repositoryname = "APITools"
url = "https://api.github.com/repos/{}/{}/issues".format(username, Repositoryname)

counter = 0
for rec in my_dict:
    if counter == 10:
        break

    rc_name = rec['full_name']
    rc_pb_desc = rec['prob_desc']
    rc_label = rec['email_address']
    counter += 1

    token = "type your token here"
    headers = {"Authorization": "token {}".format(token)}

    # Create a list containing different issues
    my_dict = [{"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}]

    # Add a for loop to repeat the request and posting process
    for data in my_dict:
        requests.post(url, data=json.dumps(data), headers=headers)
        print("Creating Issues")
