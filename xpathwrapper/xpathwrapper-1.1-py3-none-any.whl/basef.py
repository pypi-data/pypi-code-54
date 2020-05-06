'''
Created on 06-May-2020

@author: elango
'''

"""
Usage of configuration of path

To config all path by finding element , name ..etc

"""

from selenium import webdriver
import platform

"""
Usage of import the selenium web driver

To use default configuration from Selenium web driver

"""
__all__ = ["checkbyid","checkbyname","checkbyxpath","checkbylinktext","checkbypartialtext","checkbytag",
           "checkbyclass","checkbycss","checkbynames","checkxpathelements","checkbylinktexts","checkbypartialtexts",
           "checkbytagelements","checkbyclassnames","checkbycssselectors"]

"""
Check the Platform to perform the browser
"""
try:
    w = platform.system()
    if ("Windows" == w):
        driver = webdriver.Firefox(executable_path='\\drivers\\geckodriver6.exe')
    elif (w == "Linux"):
        driver = webdriver.Firefox(executable_path='\\drivers\\geckodriver')
    elif (w == "Darwin"):
        driver = webdriver.Firefox(executable_path='\\drivers\\geckodriver')
except:
    print("Check the Browser")


"""
To create the object for web driver firefox

"""
driver.implicitly_wait(30)

#driver.get("https://oucqa.tnq.co.in/oucui/app/#/instantidentifierconfig")

"""
Assign the waiting time to run the process at every time

"""

def checkbyid(locator):
    """
    checkbyid(locator)

    Locating by Id; Use this when you know id attribute of an element. With this strategy, 
    the first element with the id attribute value matching the location will be returned.
    If no element has a matching id attribute, a NoSuchElementException will be raised..
     
    checkbyid('loginForm')
    
    """
    return driver.find_element_by_id(locator)
    
def checkbyname(locator):
    """
    checkbyname(locator)

    Locating by Name; Use this when you know name attribute of an element. With this strategy,
     the first element with the name attribute value matching the location will be returned. 
     If no element has a matching name attribute, a NoSuchElementException will be raised. 
    
    checkbyname('username')
    
    """
    return driver.find_element_by_name(locator)

def checkbyxpath(locator):
    """
    checkbyxpath(locator)

    Locating by XPath; XPath is the language used for locating nodes in an XML document. As HTML can 
    be an implementation of XML (XHTML), Selenium users can leverage this powerful language to target 
    elements in their web applications. XPath extends beyond (as well as supporting) the simple methods 
    of locating by id or name attributes, and opens up all sorts of new possibilities such as locating 
    the third checkbox on the page.

    One of the main reasons for using XPath is when you don't have a suitable id or name attribute for 
    the element you wish to locate. You can use XPath to either locate the element in absolute terms 
    (not advised), or relative to an element that does have an id or name attribute. XPath locators can 
    also be used to specify elements via attributes other than id and name.

    Absolute XPaths contain the location of all elements from the root (html) and as a result are likely 
    to fail with only the slightest adjustment to the application. By finding a nearby element with an id 
    or name attribute (ideally a parent element) you can locate your target element based on the 
    relationship. This is much less likely to change and can make your tests more robust. 
    
    checkbyxpath('/html/body/form[1]')
    
    """
    return driver.find_element_by_xpath(locator)

def checkbylinktext(locator):
    """
    checkbylinktext(locator)

    Locating Hyperlinks by Link Text; Use this when you know link text used within an anchor tag. 
    With this strategy, the first element with the link text value matching the location will be 
    returned. If no element has a matching link text attribute, a NoSuchElementException will be raised.

    checkbylinktext('Continue')
    
    """
    return driver.find_element_by_link_text(locator)
    
def checkbypartialtext(locator):
    """
    checkbypartialtext(locator)

    findFileByName; Search the file by using name of the file in directory.
    Once using name indicates the file name and path indicates the directory where
    you want to search. 
    
    checkbypartialtext('Conti')
    
    """
    return driver.find_element_by_partial_link_text(locator)

def checkbytag(locator):
    """
    checkbytag(locator)

    Locating Elements by Tag Name; Use this when you want to locate an element by tag name. 
    With this strategy, the first element with the given tag name will be returned. If no 
    element has a matching tag name, a NoSuchElementException will be raised.
    
    checkbytag('h1')
    
    """
    return driver.find_element_by_tag_name(locator)
    
def checkbyclass(locator):
    """
    checkbyclass(locator)

    Locating Elements by Class Name; Use this when you want to locate an element by class 
    attribute name. With this strategy, the first element with the matching class attribute 
    name will be returned. If no element has a matching class attribute name, a 
    NoSuchElementException will be raised. 
    
    checkbyclass('content')
    
    """
    return driver.find_element_by_class_name(locator)
    
def checkbycss(locator):
    """
    checkbycss(locator)

    Locating Elements by CSS Selectors; Use this when you want to locate an element by CSS selector
    syntax. With this strategy, the first element with the matching CSS selector will be returned.
    If no element has a matching CSS selector, a NoSuchElementException will be raised. 
    
    checkbycss('p.content')
    
    """
    return driver.find_element_by_css_selector(locator)

def checkbynames(locator):
    """
    checkbynames(locator)

    Locating by Name; Use this when you know name attribute of an element. With this strategy,
    the first element with the name attribute value matching the location will be returned. 
    If no element has a matching name attribute, a NoSuchElementException will be raised. 
    
    checkbynames('username')
    
    """
    return driver.find_elements_by_name(locator)
  
def checkxpathelements(locator):
    """
    checkxpathelements(locator)

    Locating by XPath; XPath is the language used for locating nodes in an XML document. As HTML can 
    be an implementation of XML (XHTML), Selenium users can leverage this powerful language to target 
    elements in their web applications. XPath extends beyond (as well as supporting) the simple methods 
    of locating by id or name attributes, and opens up all sorts of new possibilities such as locating 
    the third checkbox on the page.

    One of the main reasons for using XPath is when you don't have a suitable id or name attribute for 
    the element you wish to locate. You can use XPath to either locate the element in absolute terms 
    (not advised), or relative to an element that does have an id or name attribute. XPath locators can 
    also be used to specify elements via attributes other than id and name.

    Absolute XPaths contain the location of all elements from the root (html) and as a result are likely 
    to fail with only the slightest adjustment to the application. By finding a nearby element with an id 
    or name attribute (ideally a parent element) you can locate your target element based on the 
    relationship. This is much less likely to change and can make your tests more robust. 
    
    checkxpathelements('/html/body/form[1]')
    
    """
    return driver.find_elements_by_xpath(locator)

def checkbylinktexts(locator):
    """
    checkbylinktexts(locator)

    Locating Hyperlinks by Link Text; Use this when you know link text used within an anchor tag. 
    With this strategy, the first element with the link text value matching the location will be 
    returned. If no element has a matching link text attribute, a NoSuchElementException will be raised.

    checkbylinktexts('Continue')
    
    """
    return driver.find_elements_by_link_text(locator)
    
def checkbypartialtexts(locator):
    """
    checkbypartialtexts(locator)

    findFileByName; Search the file by using name of the file in directory.
    Once using name indicates the file name and path indicates the directory where
    you want to search. 
    
    checkbypartialtexts('Conti')
    
    """
    return driver.find_elements_by_partial_link_text(locator)

def checkbytagelements(locator):
    """
    checkbytagelements(locator)

    Locating Elements by Tag Name; Use this when you want to locate an element by tag name. 
    With this strategy, the first element with the given tag name will be returned. If no 
    element has a matching tag name, a NoSuchElementException will be raised.
    
    checkbytagelements('h1')
    
    """
    return driver.find_elements_by_tag_name(locator)
 
def checkbyclassnames(locator):
    """
    checkbyclassnames(locator)

    Locating Elements by Class Name; Use this when you want to locate an element by class 
    attribute name. With this strategy, the first element with the matching class attribute 
    name will be returned. If no element has a matching class attribute name, a 
    NoSuchElementException will be raised. 
    
    checkbyclassnames('content')
    
    """
    return driver.find_elements_by_class_name(locator)
    
def checkbycssselectors(locator):
    """
    checkbycssselectors(locator)

    Locating Elements by CSS Selectors; Use this when you want to locate an element by CSS selector
    syntax. With this strategy, the first element with the matching CSS selector will be returned.
    If no element has a matching CSS selector, a NoSuchElementException will be raised. 
    
    checkbycssselectors('p.content')
    
    """
    return driver.find_elements_by_css_selector(locator)
