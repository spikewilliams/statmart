# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd 
import urllib
import csv
import sys, os
from time import strftime
import json
import urllib
import http.client
import base64

proot = "C:/Users/rwilliams/Documents/portal/"
profiledir = proot + "content/profiles/"
profileoutputdir = proot + "data/profiles/"

# <codecell>

#utility functions

chatter = False
def elog(s):
    if chatter:
        print(s)

def formatComputerReadableString(strn):
    return(strn.strip().lower().replace(" ","-"))

# <codecell>

# this is used to massage the individual sheets in the .xls file, to ensure it ends up nicely formatted

def processSheet(name, df, country):
    description = "ECLAC country profile - " + country
    
    if name == "quick-facts":
        description = description + ": Quick facts"
        df.columns =  ["field","value"]
        df["field"] = df["field"].map(formatComputerReadableString)
        
        #add value calculations here
        pop = int(df[df["field"] == "population"]["value"])
        la = float(df[df["field"] == "land-area"]["value"])
        dense = pop/la
        df = pd.concat([df,pd.DataFrame([["density",dense]], columns = ["field","value"])])
        
    elif name == "government-officials":
        description = description + ": Government officials"
        df.columns =  ["title","name","link"]
        
    elif name == "budget-documents":
        description = description + ": Budget documents"
        df.columns =  ["title","link"]

    elif name == "media":
        description = description + ": Local media"
        df.columns =  ["name","type","link","feed"]
        df = df.sort(["name"])
        
    else: #all other sheets are ignored
        return ("","")
    
    return (df, description)

# <codecell>

#split up the various sheets of the profile_country.xls file into .csv files

def turnXLSProfilesIntoCSV():
    c = open (proot + "Countries.txt","r")
    rows = []
    for country in c.readlines():
        country = country.strip()
        elog(country)
        lcountry = formatComputerReadableString(country)
        profile = profiledir + "profile_" + lcountry + ".xls"
        if not os.path.isfile(profile):
            elog("Missing profile: " + profile)
            continue
        xlfile = pd.ExcelFile(profile)
        for sheetname in xlfile.sheet_names:
            sheet = xlfile.parse(sheetname)
            (sheet, description) = processSheet(sheetname, sheet, country)
            if len(sheet) == 0: #sheets without any data, we ignore
                continue
            filename = lcountry + "_" + sheetname + ".csv"
            filepath = profileoutputdir + filename
            #path,file_location,description
            
            sheet.to_csv(filepath, index=False)
            
            identifier = "%s/%s/%s" % ("profile",lcountry,sheetname)
            rows.append([identifier,filename,description])

    # return some metadata about the files, which we can later use to tell TDT about our .csv files
    return pd.DataFrame(rows, columns=["identifier","filename","description"])

tdtdf = turnXLSProfilesIntoCSV()

# <codecell>

#a bunch of configuration and security stuff used by TDT's REST API

username = "admin"
password = "admin"
apiroot = "http://drupal01/data/api/definitions/"
hostname = "drupal01"

encodestring = '%s:%s' % (username, password)
auth = base64.encodebytes(encodestring.encode('utf-8'))[:-1]
auth =  ("%s" % auth)[2:-1]


#this function makes the REST API call to inform the TDT server about the .csv files

def putDefinitionCSV(path,file_location,description,title,delimiter=",",has_header_row="1",start_row="0",
                     pk="",date=None,source="",language="English",rights="License Not Specified"):
    if date == None:
        date = strftime("%Y-%m-%d %H:%M:%S")
    
    data = {"type":"csv",
            "uri":file_location,
            "description":description,
            "delimiter":delimiter,
            "has_header_row":has_header_row,#string or int?
            "start_row":start_row,
            "pk":"",
            "title":title,
            "date":date,
            "source":source,
            "language":language,
            "rights":rights}

    h = http.client.HTTPConnection(hostname)
    headers = {"Content-Type":"application/tdt.csv", 
               "Accept":"*/*", 
               "Authorization":"Basic %s" % auth}
    elog(json.dumps(data))
    h.request('PUT', apiroot + path, json.dumps(data), headers)
    r = h.getresponse()
    h.close()
    j = ("%s" % r.read())[2:-1]
    if j:
        return json.loads(j)
    return None

# <codecell>

#TODO: move the .csv files onto the server - this is handled manually for now

droot = "/www/datatank/data/profiles/" #this is the path the the directory of files on the server

#tell TDT about the .csv files

for index in tdtdf.index:
    line = tdtdf.ix[index]
    ident = line["identifier"]
    fpath = droot + line["filename"]
    descr = line["description"]
    putDefinitionCSV(ident, fpath, descr, descr) 

# <codecell>

chatter = True

# <codecell>


