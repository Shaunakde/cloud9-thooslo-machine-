# -*- coding: utf-8 -*-
"""
Created on Thu May 07 16:36:42 2015

@author: shaunakDe
"""

import csv
import re
import cookielib
import urllib2
import time
from bs4 import BeautifulSoup



def remove_common_elements(a, b):
    a_new = a[:]
    b_new = b[:]
    for i in a:
        if i in b_new:
            a_new.remove(i)
    return a_new

def makeList(location, language):
    sleepout = 15
    increment = 15
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPSHandler(debuglevel=0),urllib2.HTTPCookieProcessor(cookies))
    opener.addheaders = [('User-agent', 'Crawler_ClrFeed/1.0')]
    #https://github.com/search?l=Objective-C&p=1&q=language%3AObjective-C+location%3A%22San+Francisco%22&ref=advsearch&type=Users&utf8=%E2%9C%93
    #page='1'

    masterList = []
    page = 1
    loc = urllib2.quote(location)
    #loc = urllib2.quote('Palo Alto')
    langg = urllib2.quote(language)
    #langg = urllib2.quote('Objective-C')
    try:
        while page < 101:
            pagez=str(page)
            searchstring = r'https://github.com/search?l=Objective-C&p='+pagez+r'&q=language%3A'+langg+'+location%3A%22'+loc+'%22&ref=advsearch&type=Users&utf8=%E2%9C%93'

            try:
                response = opener.open(searchstring)
                sleepout = 30
                print 'We are good! Sleepout:%d Page:%d'%(sleepout,page)
                #print  dict(response.info())
            except urllib2.HTTPError as e:
                if e.code == 429:
                    print 'Slowing down the action! %d'%(sleepout)
                    time.sleep(sleepout)
                    sleepout = sleepout + increment
                    continue

            the_page = response.read()
            http_headers = dict(response.info())



            soup = BeautifulSoup(the_page)

            outputS = ''

            results = soup.findAll('a')
            for link in results:
                outputS = outputS + link['href'] + '\n'

            reg = re.compile(r'(/[a-zA-Z0-9]*)[\n]')
            lists = re.findall(reg, outputS)

            lists = list(set(lists))

            common = ['/about','/','/explore','/contact','/join','/features','/security','/terms','/privacy','/blog']
            lists = remove_common_elements(lists,common)
            masterList.extend(lists)
            if lists == []:
                print 'We are done here.'
                break; #no more!
            page = page+1
            print lists

            #time.sleep(1)
    #except Exception as inst:
    #    print http_headers

    finally:
        f = open('Github/githubList'+loc+'-'+langg+'.csv','wb')
        fcsv = csv.writer(f)
        for row in masterList:
            fcsv.writerow([row])
        f.close()
    #(/[a-zA-Z0-9]*)[\n]

locations = ['Boston', 'Seattle', 'Washington', 'San Francisco', 'Palo Alto', 'New York', 'Ohio', 'Tokyo', 'Milan','London', 'Los Angeles', 'Chicago', 'Houston', 'Mumbai','Pune', 'Lucknow', 'Banglore', 'Hyderabad', 'Kolkata', 'Chennai', 'Delhi', 'Ahemdabad', 'Surat' ,'Singapore']
languages = ['Objective-C', 'swift', 'C', 'C++', 'Ruby', 'PHP', 'Python', 'Java', 'JavaScript', 'Scala']
for loc1 in locations:
    for lan1 in languages:
        makeList(loc1,lan1)