import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os

def get_departements(url):
    departements = []
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, "lxml")
    for link in soup.findAll('a'):
        try:
            if 'Département' in link['title']:
                departements.append(link['href'])
                print('Found '+ str(link['href']))
        except KeyError:
            print('Key Error in departements')
        time.sleep(0.1)
    return departements

def get_mairies(base_url, departements_list):
    mairies = []
    for departement in departements_list:
        url = str(base_url) +str(departement)
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.findAll('a'):
            try:
                if 'Mairie' in link['title']:
                    mairies.append(link['href'])
                    print('Found ' + str(link['href']))
            except KeyError:
                print('Key error in mairies')
        time.sleep(0.1)
    return mairies


def get_mails(base_url, mairies):
    mails = []
    for mairie in mairies:
        url = str(base_url)+ str(mairie)
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.text, "lxml") 
        for link in soup.findAll('a'):
            try:
                testlink = link['href']
            except KeyError:
                testlink = ' '
            if 'mailto:' in testlink:
                mail = testlink[7:]
                writefile(mail)
                print(mail)
                mails.append(mail)
                time.sleep(0.01)
            
            else:
                pass
    return mails

def writefile(word):
    with open("/home/simon/Documents/Code/Python/web_scrapping/mairies_mail/emails.txt", "a") as fh:
        fh.write(word+"\n")
    os.chmod("/home/simon/Documents/Code/Python/web_scrapping/mairies_mail/emails.txt", 0o777)
 
    

def main():
    url="https://www.adresses-mairies.fr/"
    departements = get_departements(url)
    mairies = get_mairies(url, departements)
    mails = get_mails(url, mairies)
    print(mails)

main()