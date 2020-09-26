'''
Author: tkogucki

Repositories borrowed from: https://github.com/codingforentrepreneurs/30-Days-of-Python.git

Items used: inbox.py of day 9 to help with access Gmail

'''

import getpass
import imaplib
import email
import csv

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
    _, search_data = mail.search(None, 'UNSEEN')
    return search_data



def main():
    search_data = authenticate()

if __name__ == '__main__':
    main()
