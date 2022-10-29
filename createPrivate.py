import requests
import json

owner = "ownerName"
OnCore = "RepName"
RIME_repository = "RIME_repository"
Analytics_Repository = "Analytics_Repository"
myToken = 'TokenHere'

# ONCOR REPOSITORY DATA
OnCorUrl = f'https://api.github.com/repos/{owner}/{OnCore}/issues?state=all'
OnCor_head = {'Authorization': 'token {}'.format(myToken)}
r = requests.get(OnCorUrl, headers=OnCor_head)


def OnCor_api(apicall, header, **kwargs):
    data = kwargs.get('page', [])
    resp = requests.get(apicall, headers=header)
    data += resp.json()
    if len(data) > 500:
        return data
    if 'next' in resp.links.keys():
        return OnCor_api(resp.links['next']['url'], header, page=data)
    return data


OnCor_data = OnCor_api(OnCorUrl, OnCor_head)

# ANALYTICS REPOSITORY DATA

Analytics_Url = f'https://api.github.com/repos/{owner}/{Analytics_Repository}/issues?state=all'
Analytics_Header = {'Authorization': 'token {}'.format(myToken)}
r = requests.get(Analytics_Url, headers=Analytics_Header)


def Analytics_Api(apicall, header, **kwargs):
    data = kwargs.get('page', [])
    resp = requests.get(apicall, headers=header)
    data += resp.json()
    if len(data) > 500:
        return data
    if 'next' in resp.links.keys():
        return Analytics_Api(resp.links['next']['url'], header, page=data)
    return data


Analytics_Data = Analytics_Api(Analytics_Url, Analytics_Header)

# RIME-REPOSITORY DATA
RIMEurl = f'https://api.github.com/repos/{owner}/{RIME_repository}/issues?state=all'
RIME_Header = {'Authorization': 'token {}'.format(myToken)}
r = requests.get(RIMEurl, headers=RIME_Header)


def RIME_api(apicall, header, **kwargs):
    data = kwargs.get('page', [])
    resp = requests.get(apicall, headers=header)
    data += resp.json()
    if len(data) > 500:
        return (data)
    if 'next' in resp.links.keys():
        return Analytics_Api(resp.links['next']['url'], header, page=data)
    return data


RIME_Data = RIME_api(RIMEurl, RIME_Header)

# REDCUP DATA

data = {
    'token': 'towkenHere',
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
    'returnFormat': 'json'
}
r = requests.post('https://showmeportal.missouri.edu/redcap/api/', data=data)
print('Our Program Successfully runs' + " " + 'HTTP Status: ' + str(r.status_code))
my_dict = r.json()

# INSERT ISSUES IN ONCOR
url = "https://api.github.com/repos/{}/{}/issues".format(owner, OnCore)
if len(OnCor_data) == 0:
    for item1 in my_dict:
        if item1['issue_type'] == '16':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            requests.post(url, data=json.dumps(datas), headers=OnCor_head)
else:
    for item1 in my_dict:
        if item1['issue_type'] == '16':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            flag = False
            for item in OnCor_data:
                if item["body"] == rc_pb_desc:
                    flag = True
                    print("ast")
                    break
            if flag == False:
                requests.post(url, data=json.dumps(datas), headers=OnCor_head)
# INSERT ISSUE IN RIME REPOSITORY
url1 = "https://api.github.com/repos/{}/{}/issues".format(owner, RIME_repository)
if len(RIME_Data) == 0:
    for item1 in my_dict:
        if item1['request_type'] == '2':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            requests.post(url1, data=json.dumps(datas), headers=RIME_Header)
else:
    for item1 in my_dict:
        if item1['request_type'] == '2':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            flag = False
            for item in RIME_Data:
                if item["body"] == rc_pb_desc:
                    flag = True
                    print("ast")
                    break
            if flag == False:
                requests.post(url1, data=json.dumps(datas), headers=RIME_Header)

# INSERT ISSUES IN ANALYTICS REPOSITORY

url2 = "https://api.github.com/repos/{}/{}/issues".format(owner, Analytics_Repository)
if len(Analytics_Data) == 0:
    for item1 in my_dict:
        if item1['request_type'] == '1':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            requests.post(url2, data=json.dumps(datas), headers=Analytics_Header)
else:
    for item1 in my_dict:
        if item1['request_type'] == '1':
            rc_name = item1['full_name']
            rc_pb_desc = item1['prob_desc']
            rc_label = item1['email_address']
            datas = {"title": rc_name, "body": rc_pb_desc, "labels": [rc_label]}
            flag = False
            for item in Analytics_Data:
                if item["body"] == rc_pb_desc:
                    flag = True
                    print("ast")
                    break
            if flag == False:
                requests.post(url2, data=json.dumps(datas), headers=Analytics_Header)
print("Creating Issues")
