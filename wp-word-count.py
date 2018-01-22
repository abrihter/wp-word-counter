#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
title           : get word count from WP blogs
author          : bojan
date            : 20180121
version         : 1.0
usage           : python wp-word-count.py [params]
notes           : you can get help with --help
python_version  : 3.4
description     : script will take url list file and return word count for WP
                  blogs in list.                  
#==============================================================================
Params:
    - urls: file containing URLs to search
    - export: file to export data
    
How to use:
python3 wp-word-count.py -urls urls.txt -export data-export.csv 
#==============================================================================
v1.0 - 21.01.2018
    - first working version
"""

import requests
import argparse
import csv
import re
from lxml import html
import os.path

APP_VERSION = '1.00'

class bsspider_requests_mockup:
    '''mockup class for HTTP requests'''
    content = '<html></html>'
    
class bspider:
    '''spider class'''
    bsrm = []        
    def __init__(self):
        '''init'''
        self.bsrm = bsspider_requests_mockup()
        
    def tree_from_string(self, s):
        '''return object from string
        :param str s: string to convert to tree
        :return: returns lxml object for xpath'''
        return html.fromstring(s)
        
    def requests_url_to_tree(self, url, time_out = 10, attempt = 1,
        max_attempts = 3, custom_headers = {}):
        '''convert URL to tree for xpath
        :param str url: URL to get HTML
        :param int time_out: time out for request
        :param int attempt: attempt counter
        :param int max_attempts: max attempts to get data
        :param dict custom_headers: custom headers for request
        :retrun: returns tree for xpath
        '''
        page = self.requests_get_html(url, time_out = time_out, 
            attempt = attempt, max_attempts = max_attempts, 
            custom_headers = custom_headers)
        return self.tree_from_string(page.content)
        
    
    def requests_get_html(self, url, time_out = 10, attempt = 1,
        max_attempts = 3, custom_headers = {}):
        '''get html from URL using requests
        :param str url: HTML to get HTML
        :param int time_out: time out for request
        :param int attempt: attempt counter
        :param int max_attempts: max attempts to get data
        :param dict custom_headers: custom headers for request
        :return: returns HTML for URL
        '''
        if attempt > max_attempts:
            print('Too many attempts on URL: ' + url)
            pg = self.bsrm
        else:
            headers = { 
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) \
                 AppleWebKit/537AppleWebKit/537.36 (KHTML, like Gecko) \
                 Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0' }
            headers.update(custom_headers)
            try:
                pg = requests.get(url, timeout = time_out, headers = headers)
                if hasattr(pg, 'content') == False:
                    print('No data on URL: ' + url)
                    return self.bsrm
                else:
                    return pg
            except:
                pg = self.requests_get_html(url, time_out = time_out,
                    attempt = attempt + 1, max_attempts = max_attempts,
                    custom_headers = custom_headers)
        return pg
        
class wordcount:
    '''main class to count words on page'''
    urls = []
    spider = None
    export_file = []
    
    def __init__(self, file, export_file):
        '''init
        :param str file: input file (URLs list)
        :param str export_file: file to export data
        '''
        self.export_file = export_file
        with open(file, 'r') as f:
            self.urls = f.readlines()
            self.urls = [x.strip() for x in self.urls]
        self.spider = bspider()
        
    def insert_data_to_csv(self, fn, data, create_file = False):
        '''insert data to CSV
        :param str fn: file name
        :param list data: data to insert
        :param bool create_file: to create file pass True 
                                 (it will insert data as header)
        :retrun: returns nothing
        '''
        if create_file:
            myfile = open(fn, 'w', encoding = 'utf-8', newline = '')
        else:
            myfile = open(fn, 'a', encoding = 'utf-8', newline = '')
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)
        myfile.close()
        
    def clean_text(self, s):
        '''clean text
        :param str s: string to clean
        :retrun: clean text
        '''
        s = s.replace('\r', ' ').replace('\n', ' ')
        s = s.replace('\t', ' ').strip()
        s = ' '.join(s.split())
        return s
        
    def count(self):
        '''count words in URLs'''
        # create csv export file
        self.insert_data_to_csv(
            self.export_file, ['URL', 'Title', 'Word Count'], 
            create_file = True)
        for url in self.urls:
            # get tree
            tree = self.spider.requests_url_to_tree(url)
            # extract text
            d = tree.xpath('//div[@class="entry-content"]')
            text = d[0].text_content() if len(d) > 0 else ''
            text = self.clean_text(text)
            # extract title
            d = tree.xpath('//h1[contains(@class, "entry-title")]')
            title = d[0].text_content() if len(d) > 0 else ''
            title = self.clean_text(title)           
            #get count
            words = re.findall('\d*\.?\d*\w+', text)
            words_count = len(words)
            #write to export file
            data = [url, title, words_count]
            print(data)
            self.insert_data_to_csv(self.export_file, data)
            
if __name__ == '__main__':
    print('*****************')
    print('* WP word count *')
    print('*****************')
    print('Version: {0}'.format(APP_VERSION))
    parser = argparse.ArgumentParser()
    parser.add_argument("-urls", dest = "urls", default = "", 
        help="file with list of urls")
    parser.add_argument("-export", dest = "export", default = "", 
        help="file to export data to")
    args = parser.parse_args()
    if args.urls != '':
        if not os.path.isfile(args.urls):
            print('Please enter valid file for urls parameter!')
            exit()
    else:
        exit()
    if args.export == '':
        print('Please enter valid file name for export file!')
        exit()
    #run app
    counter = wordcount(args.urls, args.export)
    counter.count()
    