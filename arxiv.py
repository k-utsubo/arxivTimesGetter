#!/bin/env python
# coding:utf-8


import argparse
import json
import lxml.html
import urllib.request
import re
import time
import os
URL="https://github.com/arXivTimes/arXivTimes/issues/"

parser = argparse.ArgumentParser(description='')
parser.add_argument('--fm', default=1,type=int)
parser.add_argument('--to', default=1331,type=int)
parser.add_argument('--out', default="list.txt",type=str)
args = parser.parse_args()
print(json.dumps(args.__dict__, indent=2))
if os.path.exists(args.out):
    os.remove(args.out)
for i in range(args.fm,args.to+1):
    try:
        html = urllib.request.urlopen(URL+"/"+str(i)).read().decode("utf-8")
        html = re.sub("\r", "", html)
        html = re.sub("\n", "", html)
        doc = lxml.html.fromstring(html)
        #header=doc.xpath('//div[@id="partial-discussion-header"]')
        title=doc.xpath('//span[@class="js-issue-title"]')[0].text
        title=title.strip()
        #print(title)
        tbl=doc.xpath('//td[@class="d-block comment-body markdown-body  js-comment-body"]/p')
        #print(tbl[0].text)
        body=tbl[0].text
        idx=1
        for j in range(2):
            if tbl[idx].xpath("./a[@rel='nofollow']"):
                a=tbl[idx].xpath("./a")
                href=a[0].attrib["href"]
                #print(a[0].attrib["href"])
                break
            idx+=1
        #else:
        #    href=tbl[idx].text
            #print(tbl[1].text)
        #print(tbl[2].text)
        idx+=1
        author=tbl[idx].text
        with open(args.out, "a") as f:
            f.write(str(i)+"\t"+title+"\t"+href+"\t"+author+"\t"+body+"\n")
        print(i,",",title,",",href,",",author,",",body)
    except:
        pass
    time.sleep(1)

