# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:26:48 2017

@author: DGoller
"""

###############################################################################
#                                   Modules                                   #
###############################################################################

from bs4 import BeautifulSoup
#import mechanize
import lxml.html
import csv
#import urllib.request
import pandas as pd
from pandas import ExcelWriter
from urllib.request import Request, urlopen

###############################################################################
#                              Prespecifications                              #
###############################################################################




front="http://www.transfermarkt.de/jumplist/startseite/verein/"

A=[]
B=[]
C=[]
N=[]
R=[]

TNumbers=[27,16,15,18,44,33,39,82,3,41,4795,167,86,105,533,24,60,23826]         #Numbers in TM.de for the 18 BL1 Clubs
for x in TNumbers:
    back=x

    url=front+str(back)                       # Specify the URL




###############################################################################
#                              Code                                           #
###############################################################################

#request = urllib.request.Request(url)                                           # Query the website
#response = urllib.request.urlopen(request)                                      # get the code from the webpage



    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()


    soup = BeautifulSoup(webpage, "lxml")                                          # Parse the html and store it in the "soup" Variable

    table1=soup.find_all('table',class_='items')                     # Get the right table

###############################################################################
#                 find and structure the players & values                     #
###############################################################################

    table2=str(soup.find_all('div',class_='table-header'))                     # Teamname
    aa=table2[:80].find("Kader von ")+1+9
    ae=table2[aa:aa+35].find("\t")+aa
    team=table2[aa:ae]


    for row in table1[0].findAll('tr',class_='odd'):
        cells = row.findAll("td")
        rn=str(cells[0])
        ra=rn.find("rn_nummer")+11
        re=rn[ra:].find("</div")+ra
        R.append(rn[ra:re])
        namesrow = str(cells[2])
        na=namesrow.find("title=")+7
        ne=namesrow[na:].find("/><")-1+na
        N.append(namesrow[na:ne])
        pos=str(cells[4])
        pe=pos.find("</td>")
        A.append(pos[4:pe])
        val=str(cells[8])
        ve=val[29:50].find("€")+29+1
        B.append(val[29:ve])
        C.append(team)
    

    for row in table1[0].findAll('tr',class_='even'):
        cells = row.findAll("td")
        rn=str(cells[0])
        ra=rn.find("rn_nummer")+11
        re=rn[ra:].find("</div")+ra
        R.append(rn[ra:re])
        namesrow = str(cells[2])
        na=namesrow.find("title=")+7
        ne=namesrow[na:].find("/><")-1+na
        N.append(namesrow[na:ne])
        pos=str(cells[4])
        pe=pos.find("</td>")
        A.append(pos[4:pe])
        val=str(cells[8])
        ve=val[29:50].find("€")+29+1
        B.append(val[29:ve])
        C.append(team)
        

df=pd.DataFrame(N,columns=['Name'])
df['Team']=C
df['Position']=A
df['Number']=R
df['Marketvalue']=B



writer = ExcelWriter('TMvalueloop.xlsx')
df.to_excel(writer, index=False)
writer.save() 


    