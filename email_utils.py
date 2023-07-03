import os
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()
# get the host, username and password from environment variables
host = os.getenv("HostName")
username = os.getenv("email")
password = os.getenv("Password")

def get_latest_emails(host, username, password, num_emails=10):
    # set up the IMAP client
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox") # connect to the inbox.

    # search for all mail
    result, data = mail.uid('search', None, "ALL")
    # get the list of email IDs
    email_ids = data[0].split()
    # get the last num_emails email IDs
    latest_email_ids = email_ids[-num_emails:]
    emails = []
    for eid in reversed(latest_email_ids):
        result, email_data = mail.uid('fetch', eid, '(BODY.PEEK[])')
        raw_email = email_data[0][1]
        # convert bytes to string
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # get the details we want to print
        subject_header = decode_header(email_message['Subject'])[0]
        # if it's a bytes object, decode to string
        if isinstance(subject_header[0], bytes):
            subject = subject_header[0].decode(subject_header[1])
        else:
            subject = subject_header[0]

        from_header = decode_header(email_message['From'])[0]
        # if it's a bytes object, decode to string
        if isinstance(from_header[0], bytes):
            from_ = from_header[0].decode(from_header[1])
        else:
            from_ = from_header[0]

        # print the details

        ##print("Sender:", from_)
        ##print("Subject:", subject)

        # if the email message is multipart
        if email_message.is_multipart():
            for part in email_message.get_payload():
                # if the content type is text/plain
                # we extract only text
                if part.get_content_type() == "text/plain":
                    contents = part.get_payload()
                elif part.get_content_type() == "text/html":
                    # if the email content is html
                    soup = BeautifulSoup(part.get_payload(), "html.parser")
                    contents = soup.prettify()
        else:
            # if the email is not multipart
            if email_message.get_content_type() == "text/plain":
                contents = email_message.get_payload()
            elif email_message.get_content_type() == "text/html":
                # if the email content is html
                soup = BeautifulSoup(email_message.get_payload(), "html.parser")
                contents = soup.prettify()

        ##print("Contents:", contents)
        ##print("----------------------")

        emails.append({"from": from_, "subject": subject, "contents": contents})
    return emails

def get_latest_emails_fixed():
    return get_latest_emails(os.getenv("HostName"), os.getenv("email"), os.getenv("Password"))

# call the function
##get_latest_emails(host, username, password)
