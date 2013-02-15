"""Author: Matthew Darling
E-mail: matthewjdarling@gmail.com

Provides methods to get results from the Oracle of Objects website for the odds of co-ocurrence of objects,
as well as the items that would most likely be in an image with a queried object.

Uses the helper method strip_html to clean up the HTML version of the site downloaded through the urllib.urlopen() method.

proximity('dog') will return a dictionary of object: probability containing the ten objects most likely to be in an image with a dog in a random order.

coocurrence1('bone','dog) will return a float for the probability of finding a bone in an image with a dog.

Likewise, coocurrence2('bone','house','dog') will return a float for the probability of finding both a bone and a house in an image with a dog.

coocurrence3('bone','house','child','dog') returns a float for the probability of finding a bone, a house and a child in an image with a dog."""

import urllib
import re

def strip_html(value):
    """Takes and returns a string and strips the HTML tags stripped. 
    
    Also removes some potential problems from the string."""
    value = re.sub(r'<[^>]*?>', '', value)
    value = re.sub(r'2em\s1em\s1em\s1em', '', value)
    value = re.sub(r'Step\s\d', '', value)
    return value

def coocurrence1(fact1, query):
    """Takes fact1, query as strings and calculates the odds of fact1 appearing in an image with query.
    
    Returns the odds of co-ocurrence as a float."""
    tempparams = urllib.urlencode({'fact1': fact1, 'query': query, 'submitform': 'Ask the Oracle &raquo;'})
    temppage = urllib.urlopen("http://ing.utalca.cl/~castudillo/research/pkb/co_ocurrence/action.php", tempparams)
    tempstring = ''
    tempstring = tempstring + temppage.read()
    tempstring = strip_html(tempstring)
    foundAnswer = re.compile('\d\.\d*')
    tempAnswer = foundAnswer.search(tempstring)
    answer = '' + tempAnswer.group()
    answer = float(answer)
    return answer

def coocurrence2(fact1, fact2, query):
    """Takes fact1, fact2, query as strings and calculates the odds of fact 1 and fact2 appearing in an image with query.
    
    Returns the odds of co-ocurrence as a float."""
    tempparams = urllib.urlencode({'fact1': fact1, 'fact2': fact2, 'query':query, 'submitform': 'Ask the Oracle &raquo;'})
    temppage = urllib.urlopen("http://ing.utalca.cl/~castudillo/research/pkb/co_ocurrence/action.php", tempparams)
    tempstring = ''
    tempstring = tempstring + temppage.read()
    tempstring = strip_html(tempstring)
    foundAnswer = re.compile('\d\.\d*')
    tempAnswer = foundAnswer.search(tempstring)
    answer = '' + tempAnswer.group()
    answer = float(answer)
    return answer


def coocurrence3(fact1,fact2,fact3,query):
    """Takes fact1, fact2, fact3, query as strings and calculates the odds of fact1, fact2, and fact3 appearing in an image with query.
    
    Returns the odds of co-ocurrence as a float."""
    tempparams = urllib.urlencode({'fact1': fact1, 'fact2': fact2, 'fact3': fact3, 'query':query, 'submitform': 'Ask the Oracle &raquo;'})
    temppage = urllib.urlopen("http://ing.utalca.cl/~castudillo/research/pkb/co_ocurrence/action.php", tempparams)
    tempstring = ''
    tempstring = tempstring + temppage.read()
    tempstring = strip_html(tempstring)
    foundAnswer = re.compile('\d\.\d*')
    tempAnswer = foundAnswer.search(tempstring)
    answer = '' + tempAnswer.group()
    answer = float(answer)
    return answer


def proximity(query):
    "Takes query as a string and returns a dictionary of object: probability representing the ten most likely objects to find in a picture with query, and the probability of finding each of them."
    tempparams = urllib.urlencode({'query': query, 'submitform': 'Ask the Oracle &raquo;'})
    temppage = urllib.urlopen("http://ing.utalca.cl/~castudillo/research/pkb/co_ocurrence/proximity-action.php", tempparams)
    tempstring = ''
    tempstring = tempstring + temppage.read()
    tempstring = strip_html(tempstring)
    foundAnswer = re.compile('\w*\s\d.*\d*')
    tempAnswer = foundAnswer.findall(tempstring)
    stringAnswer = '\n'.join(tempAnswer)
    tempDict = re.split('\s', stringAnswer)
    dict = {tempDict[0]:tempDict[1], tempDict[2]:tempDict[3], tempDict[4]:tempDict[5], tempDict[6]:tempDict[7], tempDict[8]:tempDict[9], tempDict[10]:tempDict[11], tempDict[12]:tempDict[13], tempDict[14]:tempDict[15], tempDict[16]:tempDict[17], tempDict[18]:tempDict[19]}
    return dict
