#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2
import re
import time


def get_links(root_url):
    page = urllib2.urlopen(root_url)
    soup = BeautifulSoup(page.read(), 'html.parser')
    page.close()
    links_list = []
    for link in soup.find_all('a'):
        links_list.append(link.get('href'))
    return links_list


def clean_links(links_list):
    next_pat = re.compile(r"^(http(s)?\:\/\/)?(www\.)?(reddit\.com\/r\/DeepIntoYou[tT]ube)\/\?count=\d+&after=\w+.+$")
    vid_pat  = re.compile(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/watch\?.+$")
    
    next_link = None
    vid_links = []

    for link in links_list:
         try:
            if(vid_pat.match(link)):
                 vid_links.append(link)
            if(next_pat.match(link)):
                 next_link = link
         except TypeError:
            pass
    return [vid_links, next_link]
def main():
    root = "https://www.reddit.com/r/DeepIntoYouTube/"
    
    video_links = []

    links = get_links(root)
    cleaned_links = clean_links(links)
     
    for cleaned_link in cleaned_links[0]:
        print cleaned_link

    video_links = video_links + cleaned_links[0]
    next_link = cleaned_links[1]
    page_no = 2
    while(next_link != None):
        links = get_links(next_link)
        cleaned_links = clean_links(links)
        #print "Getting links on Page:", page_no
        for cleaned_link in cleaned_links[0]:
            print cleaned_link 
        video_links = video_links + cleaned_links[0]
        next_link = cleaned_links[1]
        #print "Next Page:", next_link
        page_no+=1
        print "Waiting...."
        time.sleep(10)








if __name__ == "__main__":
    main() 


