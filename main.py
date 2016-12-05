# coding=utf8

import urllib2
import os
import sys
from bs4 import BeautifulSoup
import re

def find_title(first_page):
    title = first_page.find('div', id='gd2').find('h1', id='gj').get_text()
    print title
    title = title.replace("/", "_")
    if (os.path.exists(title)):
        print "Already Downloaded"
        return None
    else:
        os.mkdir(title)
        return title

def download_img(url, path, index):
    fails = 0
    while True:
        try:
            if fails > 3:
                print "Page %d Download Fail." % index
                print "Image Url: " + url
                break
            print "Downloading Page %d" % index
            file = urllib2.urlopen(url)
        except:
            fails += 1
            print "Downloading Page %d Fail %d" % (index, fails)
        else:
            with open(path, "wb") as code:
                code.write(file.read())
            print "Downloaded Page %d" % index
            break

def open_page(url, title):
    index = 0
    last_page = None
    current_page = url
    while True:
        index += 1
        if (last_page == current_page):
            break
        else:
            page_fails = 0
            while True:
                try:
                    if page_fails > 3:
                        print 'Page %d Open Failed' % index
                        print 'Download Failed'
                        return
                    print "Opening Page %d" % index
                    content = urllib2.urlopen(current_page)
                    # print content.read()
                    open_page = BeautifulSoup(content.read(), 'lxml')
                except:
                    page_fails += 1
                    print "Opening Page %d Fail %d" % (index, page_fails)
                else:
                    # img_url = open_page.find('img', id='img')['src']
                    img = open_page.find('img', onerror=re.compile(r"this.onerror=null"))
                    img_url = img['src']
                    path = os.path.join(title, "%02d" % index + os.path.splitext(img_url)[1])
                    download_img(img_url, path, index)
                    last_page = current_page
                    # current_page = open_page.find('div', id='i3').find('a')['href']
                    current_page = img.parent['href']

                    break

if __name__ == '__main__':
    hentai_url = sys.argv[1]
    if hentai_url is None:
        print "The Url Can NOT Be Nil"
        exit()
    main_page = BeautifulSoup(urllib2.urlopen(hentai_url).read(), 'lxml')
    title = find_title(main_page)
    index = 0
    if title is not None:
        open_page(main_page.find('div', class_='gdtm').find('a')['href'], title)
    else:
        exit()