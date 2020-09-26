'''
Author: tkogucki

Repositories borrowed from: https://github.com/codingforentrepreneurs/30-Days-of-Python.git

Items used: inbox.py of day 9 to help with access Gmail

'''

import getpass
import imaplib
import email
import csv

# class containing individual email information
class Email():
    def __init__(self, subject, e_to, e_from, date):
        self.subject = subject
        self.e_to = e_to
        self.e_from = e_from
        self.date = date
        self.body = ''
        self.html_body = False

#Authenticate Function
def authenticate(file = 'username.txt'):
    host = 'imap.gmail.com'
    with open(file) as csv_file:
            file_content = csv.reader(csv_file, delimiter = ',')
            second_column = []
            for row in file_content:
                second_column.append(row[1])
    username = second_column[0]

    p = getpass.getpass('Password: ')
    # code from source: coding for entrepaneurs day 9
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, p)
    mail.select("Weight")
    _, search_data = mail.search(None, 'ALL')
    return search_data, mail

def email_data_extraction(search_data, mail):
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        # depositing individual properties of email into class
        curr_email = Email(email_message['subject'], email_message['to'], email_message['from'], email_message['date'])
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                curr_email.body = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                curr_email.body = html_body.decode()
                curr_email.html_body = True
        my_message.append(curr_email)
    print(my_message)
    print(my_message[1].body)
    print(my_message[1].e_from)
 

def main():
    search_data, mail = authenticate()
    email_data_extraction(search_data, mail)

    mail.logout()

if __name__ == '__main__':
    main()
