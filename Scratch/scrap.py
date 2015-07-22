import csv
import re
import cookielib
import urllib2

from bs4 import BeautifulSoup



#outf = open('output.csv','w+')
f = open('IND.csv','wb')
outf = csv.writer(f)

outf.writerow(['Name','GitHub', 'Handle', '#Repos', 'Language1', 'Language2', 'Language3', 'Location', 'email', 'ContributionsThisYear', 'Followers', 'Starred'])


with open('consolidatedIndia.csv') as csvfile:
    r = csv.reader(csvfile)
    for row in r:
        try:
            github='http://github.com'+row[0]
            repo  =row[0]+'?tab=repositories'
        except:
            github = ''
        
        #print github
        
        try:
            cookies = cookielib.CookieJar()
            
            opener = urllib2.build_opener(
                         urllib2.HTTPRedirectHandler(),
                         urllib2.HTTPHandler(debuglevel=0),
                         urllib2.HTTPSHandler(debuglevel=0),
                         urllib2.HTTPCookieProcessor(cookies))
            
            response = opener.open(github)
            the_page = response.read()
            http_headers = response.info()
            
            #Playtest the logic with saving the profile
            #f = open('data/test%s.txt'%(github[-5:]),'w+')
            #f.write(the_page)
            
            # git hub uses a meta tag: 
            # <meta name="description" content="toddlee has 7 repositories written in 
            # Objective-C, Ruby, and C++. Follow their code on GitHub.">
            # We can use the meta-tag for a quick list
            soup = BeautifulSoup(the_page)
            descriptionLine = soup.findAll(property='og:description')[0]['content']
            print descriptionLine

            l = 0

            reg = ur'(.*) has ([0-9]*) repositories written in ([\w+-]*),\s([\w+-]*),\sand\s(\w*).\s(.*)'
            matchObj = re.match(reg, descriptionLine)
            l = 3
            if matchObj is None:
                reg = ur'(.*) has ([0-9]*) repositories written in ([\w+-]*) and ([\w+-]*)(.*)'
                matchObj = re.match(reg, descriptionLine)
                l = 2
                if matchObj is None:
                    reg = ur'(.*) has ([0-9]*) repositories written in ([\w+-]*).\s(.*)'
                    matchObj = re.match(reg, descriptionLine)
                    l = 1
                    if matchObj is None:
                        reg = ur'(.*) has ([0-9]*) repository(.*)'
                        matchObj = re.match(reg, descriptionLine)

            if l==3:
                handle = matchObj.group(1)
                noRepos =  matchObj.group(2)
                lang1 = matchObj.group(3)
                lang2 = matchObj.group(4)
                lang3 = matchObj.group(5)
            elif l==2:
                handle = matchObj.group(1)
                noRepos =  matchObj.group(2)
                lang1 = matchObj.group(3)
                lang2 = matchObj.group(4)
                lang3 = ''
            elif l==2:
                handle = matchObj.group(1)
                noRepos =  matchObj.group(2)
                lang1 = matchObj.group(3)
                lang2 = ''
                lang3 = ''
            elif l==1:
                handle = matchObj.group(1)
                noRepos = matchObj.group(2)
                lang1 = ''
                lang2 = ''
                lang3 = ''
            else:
                handle = matchObj.group(1)
                noRepos = ''
                lang1 = ''
                lang2 = ''
                lang3 = ''

                #matchObj.group(6)

            try:
                location = soup.findAll(itemprop='homeLocation')[0].contents[1]
            except:
                location = ''
            try:
                email = soup.findAll('a',class_='email')[0]['href'].split(':')[1]
            except:
                email = ''
            try:
                contrib = soup.findAll('span',class_='contrib-number')[0].contents[0]
            except: 
                contrib = '0'
            try:
                followers = soup.findAll('strong',class_='vcard-stat-count')[0].contents[0]
                starred = soup.findAll('strong',class_='vcard-stat-count')[1].contents[0]
            except:
                followers = '0'
                starred = '0'
            try:
                site = soup.findAll('a',class_='url')[0].contents[0]
            except:
                site = ''
            
            try:
                fname = soup.findAll('span',class_='vcard-fullname')[0].contents[0]
            except:
                fname = ''
            
                

            #vcard-stat-count
            
            
            # We can also read the repolist to check ourselves
            # https://github.com/schwa?tab=repositories
            # check the page for keywords like i-OS etc
            output = [ fname, github , handle, noRepos, lang1, lang2, lang3, location, email, contrib, followers, starred, site ]
            #xx = ','.join(output)
            #print(xx)
            outf.writerow(output)

            #break
        
        except Exception as inst:
            print 'Skipped'
            print inst
            #outf.write('\n')
            outf.writerow([])
            continue
f.close()