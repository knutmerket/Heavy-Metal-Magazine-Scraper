#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 19:55:28 2018

@author: knut
"""

import os
import requests
from selenium import webdriver
import time

browser = webdriver.Firefox()

os.makedirs('./Heavy Metal Magazine', exist_ok=True)
os.chdir('./Heavy Metal Magazine')

browser.get('https://archive.org/details/heavy-metal-magazine')

try:
################# Code below needed to scroll and load the last couple of magazines (page 2). Shamelessly copied from https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python ####################
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
################# End of scroll section ####################
    
    
    print('Creating and populating list with magazine URLs...')
    linkList = []
    for i in browser.find_elements_by_css_selector('.item-ttl.C.C2'):
        linkList.append(i.find_element_by_css_selector('a').get_attribute('href'))
    print('Found %s magazine URLs.' % len(linkList))


    for i in linkList:
        browser.get(i)
        print('Locating .cbr or .cbz file...')
        try:
            downloadLink = browser.find_element_by_partial_link_text('COMIC BOOK')
            print('Found .cbr/.cbz file')
            try:
                print('Attempting to download file...')
                res = requests.get(downloadLink.get_attribute('href'))
                res.raise_for_status()
                fileName = downloadLink.get_attribute('href').split('/')[-1]
                saveFile = open(fileName, 'wb')
                for chunk in res.iter_content(100000):
                    saveFile.write(chunk)
                print('Download from  %s completed' % i)
            except:
                print('Issue with file download')
                continue
        except:
            print('Link to .cbr/.cbz file not found.')
            continue
    print('ALL DOWNLOADS COMPLETED! The files are located in %s' % os.getcwd())
    

except:
    print('Something went wrong!')