import urllib2
import os
import sys
from bs4 import BeautifulSoup


def find_title(first_page):
    title = first_page.find('div', id='gd2').find('h1', id='gj').get_text()
    print title
    if (os.path.exists(title)):
        print "Already Downloaded"
        return None
    else:
        os.mkdir(title)
        return title

if __name__ == '__main__':
    hentai_url = sys.argv[1]
    if hentai_url is None:
        print "The Url Can NOT Be Nil"
        exit()
    main_page = BeautifulSoup(urllib2.urlopen(hentai_url).read(), 'lxml')
    title = find_title(main_page)
    index = 0
    if title is not None:
        last_page = None
        current_page = main_page.find('div', class_='gdtm').find('a')['href']
        while True:
            index += 1
            print "Downloading Page %d"%index
            if (last_page == current_page):
                break
            else:
                open_page = BeautifulSoup(urllib2.urlopen(current_page), 'lxml')
                img_url = open_page.find('img', id='img')['src']
                file = urllib2.urlopen(img_url)
                path = os.path.join(title, "%02d" % index + os.path.splitext(img_url)[1])
                with open(path, "wb") as code:
                    code.write(file.read())
                last_page = current_page
                current_page = open_page.find('div', id='i3').find('a')['href']
    else:
        exit()