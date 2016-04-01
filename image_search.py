# ------ BING Image Search ---------
# Searches and stores the first ~20 image results
# from Bing.
#
# Scheme: Apr 2016

import urllib,urllib2,re,os,argparse

# Camelcase function for directory naming
def camelCase(string):
    k = ""
    for s in string.split():
        k = k+s.capitalize()
    return k

# Get image search query
ap = argparse.ArgumentParser()
ap.add_argument("-q","--query",required=True,help="Query string",nargs="+")
args=vars(ap.parse_args())

# Image search URL
url = "http://www.bing.com/images/search"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
arg = {}
arg["q"] = args["query"][0]
url_values = urllib.urlencode(arg)
full_url = url+"?"+url_values

# Save HTML response to a file and parse later (for testing & poor connection)
with open('data.txt','w') as f:
    response = urllib2.urlopen(full_url)
    data = response.read()
    f.write(data)
data = []
with open('data.txt','r') as f:
    data = f.read()

# Find images in BING result page
p = re.compile("href=\"[a-zA-Z0-9\\-\\.\\/\\:\\_\\+]+\" class=\"thumb\"")
parsed = p.findall(data)
print "Number of image acquired: "+str(len(parsed))
folder = "images/"+camelCase(arg["q"])
try:
    os.mkdir(folder)
except OSError:
    print "Directory already present! Continuing..."

# Retrieve every image
for i,string in enumerate(parsed):
    url_path = string[6:-15]
    p = re.compile("/[a-zA-Z0-9\\-\\.\\:\\_\\+]+")
    ftype = p.findall(url_path)
    fname = folder+"/"+str(i)+ftype[-1][1:]
    req = urllib2.Request(url_path, headers=hdr)
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        if err == "404":
            print "NOT FOUND! URL: "+url_path
            continue
        else:
            print err+" URL: "+url_path
            continue
    print url_path
    content = page.read()
    f = open(fname,"wb")
    f.write(content)
    f.close()