#!/usr/bin/python2.7

__author__ = "Bryson Tyrrell"
__version__ = "1.0"

import ast
import base64
import cookielib
from Foundation import NSAppleScript
import sys
import urllib
import urllib2
import xml.etree.cElementTree as etree

# Option to read JSS URL from 'com.jamfsoftware.jamf.plist' 
# plist_path = '/Library/Preferences/com.jamfsoftware.jamf.plist'
# import json
# import subprocess
# jssurl = json.loads(subprocess.Popen(['/usr/bin/plutil', '-convert', 'json', '-o', '-', plist_path], stdout=subprocess.PIPE).communicate()[0])['jss_url'].rstrip('/')

jssurl = "https://your.jss.org"
selfserviceuser = sys.argv[3] # Username logged into Self Service
jssusername = sys.argv[4] # JSS username
jsspassword = sys.argv[5] # JSS password
appname = sys.argv[6] # Name of the app being assigned - must match as displayed in the VPP Assignment
userextatt = sys.argv[7] # The User Extension Attribute ID
contentsearchid = sys.argv[8] # Content Search ID


class JSS:
    def __init__(self, server, username, password):
        self.server = server
        self.api_auth = base64.b64encode(username + ':' + password)
        cookiejar = cookielib.CookieJar()
        
        self.web = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        print("Authenticating to the JSS")
        self.web_request(self.server, urllib.urlencode({'username': username, 'password': password}))
            
    def api_request(self, url, data=None):
        request = urllib2.Request(url, data)
        request.add_header('Authorization', 'Basic ' + self.api_auth)  
        if data:
            request.add_header('Content-Type', 'text/xml')
            request.get_method = lambda: 'PUT'
        
        try:
            response = urllib2.urlopen(request)
            return response
        except urllib2.HTTPError as error:
            print("Resource: " + error.geturl())
            print("Message: " + error.read())
            display("An error was encountered. Please contact IT for assistance.", 0)
            sys.exit(1)
            
    def web_request(self, url, data=None):
        request = urllib2.Request(url, data)      
        try:
            response = self.web.open(request)
            return response
        except urllib2.HTTPError as error:
            print("Resource: " + error.geturl())
            print("Message: " + error.read())
            display("An error was encountered. Please contact IT for assistance.", 0)
            sys.exit(1)
            
    def vpp_content(self, searchid):
        r = self.web_request(self.server + '/advancedUserContentSearches.html?id=' +  str(searchid) + '&o=v')
        html = r.read().splitlines()
        applist = "["
        for item in html:
            if item == "\tvar data = [":
                for line in html[html.index(item) + 1:]:
                    if line == "\tvar sortable = new Array;":
                        break
                    elif line.rstrip():
                        applist += line.strip(';')[1:]
                break
        
        return ast.literal_eval(applist)
    
    def assign_app(self, user_id, ext_att_id):
        xml = "<user><extension_attributes><extension_attribute><id>{0}</id><value>Assigned</value></extension_attribute></extension_attributes></user>".format(ext_att_id)
        self.api_request(self.server + '/JSSResource/users/id/' + user_id, xml)
    
    def get_user(self, username):
        r = self.api_request(self.server + '/JSSResource/users/name/' + username)
        root = etree.fromstring(r.read())
        return root.find('id').text


def display(message, icon):
    """Icon 0 for error, 1 for app, 2 for warning"""
    print("Displaying dialog: {0}".format(message))
    applescript = '''
tell application "Self Service"
    activate
    display dialog "{0}" buttons {{"OK"}} default button "OK" with icon {1} giving up after 15
end tell'''.format(message, icon)
    dialog = NSAppleScript.alloc().initWithSource_(applescript)
    dialog.executeAndReturnError_(None)


def create_ticket():
    """This function would generate a ticket with information on the app and user
    IT staff would purchase additional seats of the app and then to assign it

    This function would be called where the number of available seats was not greater than 0
    Customize to suit your environment"""
    print("Creating ticket.")


def main():
    jss = JSS(jssurl, jssusername, jsspassword)
    content = jss.vpp_content(contentsearchid)
    for i in content:
        if i[0] == appname:
            if i[-1] > 0:
                print("There are available seats of the app.")
                userid = jss.get_user(selfserviceuser)
                print("Assigning the app.")
                jss.assign_app(userid, userextatt)
                display('{0} has been assigned to you!\n\nFind it in your App Store purchase history.'.format(appname), 1)
            else:
                print("There are not enough available seats of the app.")
                create_ticket()
                display('{0} could not be assigned at this time.\n\nA ticket has been created on your behalf. You will be contacted by IT shortly.'.format(appname), 2)


if __name__ == '__main__':
    main()
    sys.exit(0)
