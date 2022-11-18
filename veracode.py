import requests
import os
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import xml.etree.ElementTree as ET
import sys 

API_ID = sys.argv[1]
API_KEY = sys.argv[2]
filename = sys.argv[3]
env = str(sys.argv[4])
app_name = "EmpowerMobileAppOEM4"

print("app_name: ", app_name)
print("filename: ",filename)

# Get application ID from veracode
response = requests.get("https://analysiscenter.veracode.com/api/5.0/getapplist.do",
                         auth=RequestsAuthPluginVeracodeHMAC(API_ID,
                                                             API_KEY),
                         verify=None)

#parse XML response to get application ID
root = ET.fromstring(response.content)
for child in root:
     print(child.tag)
     print(child.attrib)
     if child.attrib["app_name"] == app_name:
        app_id = child.attrib["app_id"] 

print(app_id)

##get sandbox id for QA
response = requests.get("https://analysiscenter.veracode.com/api/5.0/getsandboxlist.do",
                         auth=RequestsAuthPluginVeracodeHMAC(API_ID,
                                                             API_KEY),
                         params={'app_id': app_id},
                         verify=None)

#parse XML response to get sandbox ID if QA build

root = ET.fromstring(response.content)
for child in root:
     print(child.tag)
     print(child.attrib)
     sandbox_id = child.attrib["sandbox_id"]

print(sandbox_id)
#Upload API 
#if QA upload to sandbox
if env == "qa":
    try:
        with open(filename, 'rb') as file:
            resp = requests.post('https://analysiscenter.veracode.com/api/5.0/uploadlargefile.do',
                    headers={'Content-Type': 'binary/octet-stream'},params={'app_id': app_id, 'filename': filename, 'sandbox_id':sandbox_id},
                    data=file,auth=RequestsAuthPluginVeracodeHMAC(API_ID,API_KEY))
    except Exception as err:
        print(f'Error occurred: {err}')
        # sys.exit(1)
    else:
        print(f'Req Headers: {resp.request.headers}')
        print(f'Resp Code: {resp.status_code}\nResp Text: {resp.text}')
        #Initiate prescan and scan 
        response = requests.post("https://analysiscenter.veracode.com/api/5.0/beginprescan.do",
                         auth=RequestsAuthPluginVeracodeHMAC(API_ID,
                                                             API_KEY),
                        params={'app_id': app_id, 'auto_scan': True, 'sandbox_id':sandbox_id, "scan_all_nonfatal_top_level_modules": True}
                         )

        print(response.content)

#If prod upload for normal static scan 
else: 
    try:
        with open(filename, 'rb') as file:
            resp = requests.post('https://analysiscenter.veracode.com/api/5.0/uploadlargefile.do',
                    headers={'Content-Type': 'binary/octet-stream'},params={'app_id': app_id, 'filename': filename},
                    data=file,auth=RequestsAuthPluginVeracodeHMAC(API_ID,API_KEY))
    except Exception as err:
        print(f'Error occurred: {err}')
        # sys.exit(1)
    else:
        print(f'Req Headers: {resp.request.headers}')
        print(f'Resp Code: {resp.status_code}\nResp Text: {resp.text}')
        #initiate prescan and scan
        response = requests.post("https://analysiscenter.veracode.com/api/5.0/beginprescan.do",
                         auth=RequestsAuthPluginVeracodeHMAC(API_ID,
                                                             API_KEY),
                        params={'app_id': app_id, 'auto_scan': True, "scan_all_nonfatal_top_level_modules": True})
        print(response.content)

sys.exit(0)
