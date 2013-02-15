'''
Created on 2010-12-11

Parses annotations files and creates a XML index file of objects and their locations

Once you have a dataset from LabelMe (got through labelmeretriever or otherwise),
run the main() method from the folder containing the data folder to generate an index file inside the data folder
By default, will filter out images smaller than 6000 pixels. Easy to change with the small_area variable at the top of the script.
The area of the images filtered out will be half the area specified in the variable.

Science of Imagination Laboratory

Author:Sebastien Ouellet - sebouel@gmail.com
'''

import math
import os
import sys
import re
import xml.dom.minidom

###### Variable ######

small_area = 12000.0

#######################

def find_data(further=False):
    """ Provides the path to the data directory  """
    main_directory = os.path.dirname(sys.argv[0])
    path = os.path.join(main_directory, "data")
    # To complete eventually... not much of a problem right now
    if further:
        files = os.listdir(path)
        for file in files:
            if file[-3:] != "jpg":
                path = os.path.join(path,file)
                break
    return path
   
def create_index(data_directory, list_objects):
    """ Writes an XML index file, used for searching purposes, pointing to files for each object name """
    f = open(os.path.join(data_directory,"index.xml"), "w")
    
    document = xml.dom.minidom.Document()
    index = document.createElement("index")
    document.appendChild(index)
    for old_object in list_objects:
        object = document.createElement("object")
        index.appendChild(object) 
        name = document.createElement("name")
        object.appendChild(name)
        name_text = document.createTextNode(old_object[0])
        name.appendChild(name_text)
        for location in old_object[1]:
            file = document.createElement("file")
            object.appendChild(file)
            file_text = document.createTextNode(location)
            file.appendChild(file_text)
    
    to_fix = document.toprettyxml()
    # The next two lines were written by nbolton, in a StackOverflow thread, to delete the newLine marker in the XML file
    # Will probably replace those hacky lines with the cleaner String.strip() method
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
    to_print = text_re.sub('>\g<1></', to_fix)
    f.write(to_print.encode('utf-8'))
    f.close()
    
def find_annotations(data_directory, filtering):
    """ Parses the XML annotation files for object names and file names and filters out small images """
    objects = []
    list_files = os.listdir(data_directory)
    for file in list_files:
        if file[-3:] == "xml":
            try:
                document = xml.dom.minidom.parse(os.path.join(data_directory,file))            
                for node_object in document.getElementsByTagName("object"):
                    for node_name in node_object.getElementsByTagName("name"):
                        for node_actualname in node_name.childNodes:
                            if filtering:
                                if areafilter(node_object):
                                    objects.append([node_actualname.data,file])
                            else:
                                objects.append([node_actualname.data,file])
            except xml.parsers.expat.ExpatError:
                print ""+file+" is empty"
    return objects

def areafilter(node_object):
    """ Calculates the area of an image and decides if it's too small """
    vertices_x = []
    vertices_y = []

    for node_polygon in node_object.getElementsByTagName("polygon"):
        for node_point in node_polygon.getElementsByTagName("pt"):
            for node_x in node_point.getElementsByTagName("x"):
                for node_actualx in node_x.childNodes:
                    vertices_x.append(int(float(node_actualx.data)))
            for node_y in node_point.getElementsByTagName("y"):
                for node_actualy in node_y.childNodes:
                    vertices_y.append(int(float(node_actualy.data)))

    vertices = zip(vertices_x,vertices_y)

    area = compute_area(vertices)    
    if area > small_area:
        return True
    else:
        return False

def compute_area(vertices):
    """ Compute the area of a polygon given its vertices """
    area = 0
    index = 0
    length = len(vertices)
    while index<length:
        j = (index+1)%length
        area = area + vertices[index][0]*vertices[j][1]
        area = area - vertices[index][1]*vertices[j][0]
        index = index + 1
    
    return math.fabs(area)
    
def sort_annotations(objects):
    """ Eliminates duplicate names, sorting out all locations for a single given name """
    objects.sort()
    sorted_list = [[objects[0][0],[objects[0][1]]]]
    del objects[0]
    for object in objects:
        if object[0] == sorted_list[-1][0]:
            sorted_list[-1][1].append(object[1])
        else:
            sorted_list.append([object[0],[object[1]]])
            
    return sorted_list    

def main(filtering=True):
    data_directory = find_data()
    objects = find_annotations(data_directory,filtering)
    objects = sort_annotations(objects)
    create_index(data_directory, objects)
