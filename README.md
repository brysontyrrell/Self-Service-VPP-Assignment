Self Service VPP Assignment
===========================
This Python script allows a VPP assignment to be set by a user in Self Service (i.e. for use with the Casper Suite).

Credentials for a service account to the JSS are passed as parameters along with the title of the app (as it appears when viewed in VPP Assignments), the ID of a User Extension Attribute (used for adding the JSS User to a Smart Group) and an Advanced Content Search ID that is scraped as a part of the script.

Different dialog prompts will appear depending upon whether an error was encountered, the assignment succeeded or if the assignment could not be completed.

A full write-up on this script with code explanations can be found here: https://bryson3gps.wordpress.com/

Setup in the JSS
----------------
This script allows self-assignment of **managed VPP apps** by leveraging User Extension Attributes.  For each VPP app, create a **User Extension Attribute** with the values **"Assigned"** and **"Unassigned"** as pop-up list options.  Then, for each Extension Attribute create a **Smart User Group** with the criteria being the value "Assigned" is populated.  Use this Smart Group in the corresponding **VPP Assignment's Scope** (one for each app).

Now JSS Users can be dynamically assigned a managed VPP app without directly modifying the scope.

In order to obtain the available number of seats for a managed VPP app the script scraps the HTML for an **Advanced Content Search** that displays all OS X apps and, at least, the value for **Unassigned Content**.

Using the Script
----------------
The URL for the JSS is hard coded in the script by default.  There is an alternative in the code to uncomment that will read the JSS URL from 'com.jamfsoftware.jamf.plist' instead (making this script more portable).

The following parameters are required:

- 3, Self Service Username: This is captured when a user logs into Self Service and is passed to the script.  This is used for looking up their JSS User record and possibly used if a ticket needs to be generated (see notes in the code).
- 4, JSS Service Account Username: This is the service account used by the script to access the JSS and API.
- 5, JSS Service Account Password: The password to the service account. View the repository titled "EncryptedStrings" for an option to better secure this password.
- 6, App Name: This is the name of the VPP app that must match as it is shown in the VPP Assignment.
- 7, User Extension Attribtue ID: The ID of the User Extension Attribute for the VPP app that will be updated.
- 8, Advanced Content Search ID: The ID of the Advanced Content Search for OS X apps that will be scraped by the script.

You can run the script locally by passing the required arguments as in this example (note the dashes are to pass nothing nor the first and second parameters which are not used):

```
~$ SelfServiceVPPAssignment.py - - "self.service.username" "service.account.name" "service.account.pass" "Baldur's Gate" 1 1
```
