'''
Author: tkogucki

Repositories borrowed from: https://github.com/codingforentrepreneurs/30-Days-of-Python.git

Items used: inbox.py of day 9 to help with access Gmail

'''

import getpass
import imaplib
import email
import csv
import re
from datetime import datetime

# class containing individual email information
class Email():
    def __init__(self, subject, e_to, e_from, date):
        self.subject = subject
        self.e_to = e_to
        self.e_from = e_from
        self.date = date
        self.body = ''
        self.html_body = False
        self.weight = 0
        self.date_val = None

# Authenticate Function
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

# returns list of Email classes after sorting through the email data  
def email_data_extraction(search_data, mail):
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
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
    return my_message

# filters through strings to find date and weight
def clean_data(my_messages):
    pre_string = r'<div dir="auto">'
    l_pre_string = len(pre_string)

    # use regular expressions to pull weights out of the body string
    for i in my_messages:
        x = re.findall(r'\d+\.\d+', i.body)
        if len(x) == 0:
            x = re.findall(r'\b\d+\b', i.body)
        weight = float(x[0])
        i.weight = weight
        # use datetime functionality to pull dates out of strings
        date = datetime.strptime(i.date[5:-15], r'%d %b %Y')
        i.date_val = date
#export csv
def export_csv(my_messages, file_name):
    with open(file_name, 'w', newline = "") as csvfile:
        csv_file = csv.writer(csvfile, delimiter = ',')
        header = ['Date', 'Weight [kg]', 'Weight [lbs]']
        csv_file.writerow(header)
        for i in my_messages:
            ex_value = [f'{i.date_val.month}-{i.date_val.day}-{i.date_val.year}', i.weight, i.weight * 2.20462]
            csv_file.writerow(ex_value)

def main():
    search_data, mail = authenticate()
    my_messages = email_data_extraction(search_data, mail)
    clean_data(my_messages)
    file_name = 'weights.csv'
    export_csv(my_messages, file_name)
    mail.logout()

if __name__ == '__main__':
    main()
