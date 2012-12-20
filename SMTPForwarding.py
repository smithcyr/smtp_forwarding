# By Cyrus Smith 
# (http://coding-contemplation.blogspot.com) 
# (https://github.com/smithcyr)
# 
# Small script for forwarding messages on an SMTP/IMAP server 
# where forwarding is forbidden. The script instead simply 
# has the server send unread messages from the accessed account
# to the forwarding account(s) with a few added lines at the start 
# to indicate who the message was initially from. All other 
# headers remain intact (only Sender, From and To are changed).

import imaplib
import smtplib
import email
import getpass
import sys

#-------USER ENTERED VALUES--------------
ACCESS_EMAIL = "smithcyr@grinnell.edu"
FORWARDING_ADDRESSES = "cymasm@gmail.com"
IMAPPORT = 993 # 143 # default
SMTPPORT = 587 # 25  # default
PASSWORD = "" # "youraccountpassword" 
# If you do not want to store your password just leave it blank.
# You'll be prompted each run for the password
#----------------------------------------

if not PASSWORD:
    PASSWORD = getpass.getpass("Password:",sys.stderr)
USER,HOST = ACCESS_EMAIL.split("@")
forwardmail = smtplib.SMTP("smtp."+HOST,SMTPPORT)
forwardmail.ehlo()
forwardmail.starttls()
forwardmail.ehlo
forwardmail.login(USER,PASSWORD)
newmail = imaplib.IMAP4_SSL("imap."+HOST,IMAPPORT)
# if your server does not support ssl imap then you'll need to remove
# the _SSL from the above line

newmail.login(USER,PASSWORD)
newmail.select()
typ, data = newmail.search(None, 'UnSeen')

# If unconstrained by memory/processing it is better to download all 
# emails at once and process them. That way there is less of a risk of 
# being disconnected by the imap server mid-process (and thus erroring).

#-- Memory intesive method
EMAILS = [newmail.fetch(num,'(RFC822)') for num in data[0].split()]
newmail.close()
newmail.logout()
for typ, data in EMAILS:
#--

#-- Continual connection method
#for num in data[0].split():
    #typ, data = newmail.fetch(num, '(RFC822)')
#--

    message = email.message_from_string(data[0][1])
    dochead = ("Forwarded From - " + message.__getitem__("From") + "\n" + 
               "Initially Sent To - " + message.__getitem__("To") + "\n"+"-"*45+"\n")
    newmessage = email.message.Message()
    newmessage.set_payload(dochead)
    if message.is_multipart():
        buff = message.get_payload()
    else:
        buff = email.message.Message()
        buff.set_payload(message.get_payload())
    message.set_payload([newmessage]+buff)
    if message.__contains__("Sender"):
        message.replace_header("Sender",ACCESS_EMAIL)
    message.replace_header("From",ACCESS_EMAIL)
    message.replace_header("To",FORWARDING_ADDRESSES)
    forwardmail.sendmail(ACCESS_EMAIL,FORWARDING_ADDRESSES,
    message.as_string())
    print "Processed message"

#-- Continual connection method
#newmail.close()
#newmail.logout()
#--

forwardmail.quit()

print "Forwarding Finished"
