'''
Created on 2010-12-09

Downloads folders from LabelMe. Run the main() method if you don't have a dataset. It won't work if you already have a data folder at the location.
By default, filter out all folders with 256x256 images.
For the number parameter, enter the number of folders you want to download or no number to download the whole database.
For the randomized parameter, set to True if you want the script to randomly choose folders up to the number you specified in the number parameter.

Science of Imagination Laboratory

Author: Sebastien Ouellet - sebouel@gmail.com
'''

import random
import os
import re
import urllib
import urllib2
import BeautifulSoup

def parse(website):
    """ Parse a website into a tree via BeautifulSoup """
    website_object = urllib2.Request(website)
    website_to_parse = urllib2.urlopen(website_object)
    parsed = BeautifulSoup.BeautifulSoup(website_to_parse)
    return parsed

def main(number=-1,filtering=True,randomized=False):
    data_directory = "data"
    os.makedirs(data_directory)
    
    website = "http://labelme.csail.mit.edu/Annotations"
    
    parsed = parse(website)
    folders = []
    for a in parsed.findAll('a'):
        if filtering:
            match = re.search("256x256",a.contents[0])
            if match == None:
                folders.append(a.contents[0])
        else:
            folders.append(a.contents[0])
    folders = folders[5:]
    if number == -1:
        pass
    elif randomized:
        folders = [folders.pop(random.randint(0,len(folders)-1)) for index in xrange(number)]         
    else:
        folders = folders[0:number]
    for folder in folders:
        print "Annotations for: ", folder
        website = "http://labelme.csail.mit.edu/Annotations/"+folder
        parsed = parse(website)
        for a in parsed.findAll('a'):
          if a.contents[0][-3:] == "xml":
              urllib.urlretrieve(website+a.contents[0], os.path.join(data_directory,folder[:-1]+"---"+a.contents[0]))
    for folder in folders:
        print "Images for: ", folder
        website = "http://labelme.csail.mit.edu/Images/"+folder
        parsed = parse(website)
        for a in parsed.findAll('a'):
          if a.contents[0][-3:] == "jpg":
              urllib.urlretrieve(website+a.contents[0], os.path.join(data_directory,folder[:-1]+"---"+a.contents[0]))

    
    
