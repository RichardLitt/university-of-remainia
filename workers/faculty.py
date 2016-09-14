import orcid
import csv
import requests

testorcid = '0000-0002-0068-716X'
CROSSREF_FORMAT_URL = 'http://data.crossref.org'
CROSSREF_HEADERS = {'Accept' : 'text/bibliography; style=apa; locale=en-US'}

def getresearcher(orc):
    dois = []
    researcher = orcid.get(orc)
    pubs = researcher.publications
    for pub in pubs:
        if pub.external_ids:
            for exid in pub.external_ids:
                if exid.type == 'DOI':
                    dois.append(exid.id)
            
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
    
researcher, dois = getresearcher(testorcid)
publications = "**Publications**\n\n"
for doi in dois[7:10]:
    biblioentry = formatbiblioentry(doi)
    if biblioentry:
        try:
            ref = '* %s\n' % (biblioentry)
            publications = publications + ref
        except UnicodeEncodeError:
            pass
            
funding = "**Funding**\n\n"
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

print publications
print funding    
        
