import datetime
from time import strptime
from requests import get
from bs4 import BeautifulSoup
import re

def create_datetime(times): #method for turning the time format given by the website into a datetime object
    full_date = re.split(', ',times)
    month_day = full_date[1].split()
    month_name = str(month_day[0])
    day = str(month_day[1])
    year = str(full_date[2])
    month_number = str(strptime(month_name, '%B').tm_mon)
    date = datetime.datetime.strptime(month_number + day + year, '%m%d%Y')
    return date

baseurl = 'http://www.newyorksocialdiary.com'
url = 'http://www.newyorksocialdiary.com/party-pictures'
end = False
dict = {}
while end == False:
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    namestimes = soup.find_all('span', class_ = 'field-content')
    for i in range(0,len(namestimes)-1,2):
        dict[namestimes[i+1].text] = namestimes[i].a.get('href')
    nextpage = soup.find(title = 'Go to next page')
    if nextpage:
        newurl = baseurl + nextpage.get('href')
        url = newurl
    else:
        end = True;
links = [dict[key] for key in dict if create_datetime(key) < create_datetime("Monday, December 1, 2014")]

def name_stripper(text):
    a = re.split(',| with | and |Dr\.|Mrs\.|Ms\.|Mr\.|Miss|Jr\.|\)|\\n',text)
    for i in range(0,len(a)-1):
        if len(a[i].strip().split(' ')) == 1 and a[i].strip() != '':
            a[i] += ' '
            b = a[i+1].strip().split(' ')
            for x in b[1:]:
                a[i] += x + ' '
    return [x.strip() for x in a if x.strip()!='']

def lowercase_stripper(sentence):
    a = sentence.split()
    b = []
    c= ''
    for x in a:
        if x[0].isupper():
            c += x + ' '
        else:
            if c!= '':
                b.append(c.strip())
                c = ''
    b.append(c.strip())
    return [x.strip() for x in b if x!='']
names = []
names2 = []
oldnames = []
parsednames = []
for link in links:
    url = baseurl + link
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    captions = soup.find_all('div', class_ = 'photocaption')
    oldcaptions = soup.find_all('div', class_ = 'field__item even')
    if len(oldcaptions) != 0:
        oldnames = oldcaptions[0].find_all('font')
    names += [x.text for x in captions] + [x.text for x in oldnames]
    
for a in names:
    names2 += lowercase_stripper(a)
for x in names2:
    parsednames += name_stripper(x)
            
print(len(set(parsednames)))
