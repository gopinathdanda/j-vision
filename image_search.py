#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ------ BING Image Search ---------
# Searches and stores image results from Bing.
#
# Scheme: Apr 2016

import urllib,urllib2,re,os,argparse,sys

# Camelcase function for directory naming
def camelCase(string):
    k = ""
    for s in string.split():
        k = k+s.capitalize()
    return k

# Get image search query
ap = argparse.ArgumentParser()
ap.add_argument("-q","--query",required=True,help="Query string")
ap.add_argument("-n","--num",type=int,help="Number of images required (optional, int, default = 100)")
ap.add_argument("-d","--downloadData",help="Request image query or use downloaded data (optional, yes/no, default = yes)")
ap.add_argument("-c","--continueFrom",type=int,help="Continue download from index, should be less than total number of images (optional, int, default = 1)")
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
if args["num"] is None:
    arg["count"] = 100
else:
    arg["count"] = args["num"]
url_values = urllib.urlencode(arg)
full_url = url+"?"+url_values

# Save HTML response to a file and parse later (for testing & poor connection)
if args["downloadData"] != "no":
    with open('data.txt','w') as f:
        try:
            response = urllib2.urlopen(full_url)
        except urllib2.URLError as err:
            if type(err.reason) is str:
                s = err.reason
            else:
                (e,s) = err.reason
            if s == "nodename nor servname provided, or not known":
                error = "Cannot connect"
            else:
                error = s.capitalize()
            print error
            exit()
        data = response.read()
        f.write(data)
else:
    print "Skipping image query download and using already downloaded data."
data = []
with open('data.txt','r') as f:
    data = f.read()

# Find images in BING result page
p=re.compile("imgurl:&quot;[a-zA-Z0-9\\:\\/\\.\\+\\-\\=\\_\\@\\%\\(\\)\\[\\]\\{\\}\\,\\!\\'\\’\\\\é]+[\\?\\&\\#]")
parsed = p.findall(data)
num_of_images = len(parsed)
print "Number of images acquired: "+str(num_of_images)
folder = "images/"+camelCase(arg["q"])
try:
    os.mkdir(folder)
except OSError:
    print "Directory already present. Continuing..."

# Progress bar
toolbar_width = 40
counter = 0
sys.stdout.write("#")
sys.stdout.flush()

# Calculate retrieve percentage
errors = 0

# Retrieve every image
for i,string in enumerate(parsed):
    if args["continueFrom"] is not None and i<args["continueFrom"]:
        continue
    d = open(folder+"/list.txt","a")
    url_path = string[13:-1]
    p = re.compile("/[a-zA-Z0-9\\:\\.\\+\\-\\=\\_\\@\\%\\(\\)\\[\\]\\{\\}\\,\\!\\'\\’\\\\é]+")
    ftype = p.findall(url_path)
    #print ftype
    fname = folder+"/"+str(i)+"_"+ftype[-1][1:]
    try:
        req = urllib2.Request(url_path, headers=hdr)
        page = urllib2.urlopen(req)
    except urllib2.URLError as err:
        errors = errors+1
        if type(err.reason) is str:
            s = err.reason
        else:
            (e,s) = err.reason
        if s == "nodename nor servname provided, or not known":
            error = "Cannot connect: "+url_path
        else:
            error = s.capitalize()+": "+url_path
        #print error
        d.write(error+"\n")
        continue
    except urllib2.HTTPError as err:
        errors = errors+1
        error = err.reason.capitalize()+": "+url_path
        #print error
        d.write(error+"\n")
        continue
    content = page.read()
    f = open(fname,"wb")
    f.write(content)
    f.close()
    filesize = (os.stat(fname).st_size)/float(1024)  #file size in KB
    if filesize < 3:
        os.remove(fname)
        success = "File doesn't exist or too small: "+url_path
        errors = errors+1
    else:
        success = "Received: "+url_path
    #print success
    d.write(success+"\n")
    if i*toolbar_width/num_of_images>counter:
        counter=counter+1
        sys.stdout.write("#")
    percent = ((i+1)*100/float(num_of_images))
    sys.stdout.write(" %0.2f%%" % percent)
    sys.stdout.flush()
    if percent<10:
        sys.stdout.write("\b"*6)
    else:
        sys.stdout.write("\b"*7)
sys.stdout.write("\b#")
sys.stdout.write("  100%")
sys.stdout.flush()
sys.stdout.write("\n")
print "Percentage of images retrieved: %0.2f%%" % (((num_of_images-errors)*100)/float(num_of_images))
d.close()