# ------ BING Image Search ---------
# Searches and stores image results from Bing.
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
ap.add_argument("-q","--query",required=True,help="Query string")
ap.add_argument("-n","--num",help="Number of images required (optional, default = 100)")
args = vars(ap.parse_args())

# Image search URL
url = "https://www.bing.com/images/async"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
arg = {}
arg["q"] = args["query"]
arg["async"] = "content"
arg["first"] = 0
arg["count"] = args["num"]
url_values = urllib.urlencode(arg)
full_url = url+"?"+url_values

# Save HTML response to a file and parse later (for testing & poor connection)
with open('data.txt','w') as f:
    try:
        response = urllib2.urlopen(full_url)
    except urllib2.URLError, err:
        (e,s) = err.reason
        if s == "nodename nor servname provided, or not known":
            print "CONNECTION ISSUE"
        else:
            print s.capitalize()
        exit()
    data = response.read()
    f.write(data)
data = []
with open('data.txt','r') as f:
    data = f.read()

# Find images in BING result page
p = re.compile("imgurl:&quot;[a-zA-Z0-9\\:\\/\\+\\-\\=\\_\\@\\%\\.\\?\\&]+&quot;")
parsed = p.findall(data)
print "Number of images acquired: "+str(len(parsed))
folder = "images/"+camelCase(arg["q"])
try:
    os.mkdir(folder)
except OSError:
    print "Directory already present! Continuing..."

# Retrieve every image
for i,string in enumerate(parsed):
    url_path = string[13:-6]
    p = re.compile("/[a-zA-Z0-9\\:\\-\\.\\_\\+\\@\\%]+")
    ftype = p.findall(url_path)
    fname = folder+"/"+str(i)+ftype[-1][1:]
    try:
        req = urllib2.Request(url_path, headers=hdr)
    except urllib2.URLError, err:
        (e,s) = err.reason
        if s == "nodename nor servname provided, or not known":
            print "CONNECTION ISSUE"
        else:
            print s.capitalize()
        continue
    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        print err.reason.capitalize()+": "+url_path
        continue
    content = page.read()
    f = open(fname,"wb")
    f.write(content)
    f.close()
    print "Received: "+url_path