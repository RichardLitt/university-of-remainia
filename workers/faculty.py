import orcid
import csv
import requests
import os.path
import re

testorcid = '0000-0002-0068-716X'
csvfile = 'responses.csv'
facultydirectory = "../_faculty"
CROSSREF_FORMAT_URL = 'http://data.crossref.org'
CROSSREF_HEADERS = {'Accept' : 'text/bibliography; style=apa; locale=en-US'}
md_template = """---
layout: faculty
name: %(name)s
lastName: %(lastname)s
title: %(title)s
department: %(department)s
school: %(school)s
orcid: %(orcid)s
openaire: ''
image: %(photourl)s
url: "https://twitter.com/CameronNeylon"
twitter: "https://twitter.com/CameronNeylon"
---
{%% include JB/setup %%}

%(role)s

%(euro)s

%(publist)s
%(fundinglist)s"""

def getresearcher(orc):
    dois = []
    try:
        researcher = orcid.get(orc)
    except HTTPError:
        print "Failed to retrieve ORCID"
        return None, []
    try:
        pubs = researcher.publications
        for pub in pubs:
            if pub.external_ids:
                for exid in pub.external_ids:
                    if exid.type == 'DOI':
                        if exid.id not in dois:
                            dois.append(exid.id)
    except AttributeError:
        print "Obtained no public information from ORCID\n"
        return None, []           
    return researcher, dois
    
def formatbiblioentry(doi):
    url = '{}/{}'.format(CROSSREF_FORMAT_URL, doi)
    resp = requests.get(url, headers = CROSSREF_HEADERS)
    resp.encoding = 'utf-8'
    try:
        resp.raise_for_status()
        biblioentry = resp.text
    except requests.exceptions.HTTPError:
        biblioentry = None
    return biblioentry

def formatpublicationlist(dois):
    if len(dois) == 0:
        return ""
    print "...publication list of length", len(dois)
    publications = "##Publications\n\n"
    for doi in dois:
        print ".",
        biblioentry = formatbiblioentry(doi)
        if biblioentry:
            try:
                ref = '* %s' % (biblioentry)
                publications = publications + ref
            except UnicodeEncodeError:
                pass
                
    return publications
            
def formatfundinglist(researcher):
    try: researcher.grants
    except AttributeError:
        return ""
        
    funding = "##Funding\n\n"
    for grant in researcher.grants:
        try:
            template = "* %s, %s, %d-%d, %s%s\n" % (grant.title,
                                                grant.funder,
                                                grant.start_date.year,
                                                grant.end_date.year,
                                                grant.currency,
                                                "{:,}".format(grant.value))
            funding = funding + template
        
        except UnicodeEncodeError:
                pass

    return funding

def formatorcid(raworcid, orcidregex='\\d{4}-\\d{4}-\\d{4}-\\d{3}[\\dX]'):
    rg = re.compile(orcidregex)
    match = rg.search(raworcid)
    if match:
        start,end = match.span()
        orc = raworcid[start:end]
        return orc
    else:
        return None
    
    

with open(csvfile, 'rU') as f:
    f.readline()
    faculty = csv.reader(f)
    for person in faculty:
        title = person[1]
        name = person[2]
        email = person[3]
        photourl = person[4]
        role = person[5]
        euro = person[6]
        department = person[7]
        orc = formatorcid(person[8])
        

        print "Researcher:", name, "ORCID:", orc
        print "...getting info"
        researcher, dois = getresearcher(orc)
        if not researcher:
            publicationlist = ""
            fundinglist = ""
        else:
            publicationlist = formatpublicationlist(dois)
            fundinglist = formatfundinglist(researcher)
       
        print "publist:", publicationlist
        print "funding:", fundinglist 
        pagecontent = md_template % {'name' : name,
                                     'lastname' : name.split(' ')[-1],
                                     'title' : title,
                                     'department' : department,
                                     'school' : "",
                                     'orcid' : orc,
                                     'photourl' : photourl,
                                     'role' : role,
                                     'euro' : euro,
                                     'publist' : publicationlist,
                                     'fundinglist' : fundinglist}
        
        
        filename = name.split(' ')[-1].lower() + '.md'
        filepath = os.path.join(facultydirectory, filename)
        print "...writing file"
        with open(filepath, 'w') as f:
            f.write(pagecontent.encode('utf-8'))
        print "...done\n"
        
