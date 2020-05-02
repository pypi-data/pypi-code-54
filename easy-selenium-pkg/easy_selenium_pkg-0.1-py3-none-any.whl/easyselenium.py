"""Copyright [2020] [Ankit Kothari(step2success.in)]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import time
global driver

def open_browser(headless=False,path="",browser='chrome',debug=False):
	global driver
	
	global debugs
	debugs=debug
	if browser.lower()=='chrome':
	
		chrome_options = webdriver.ChromeOptions()
		if headless:
			chrome_options.add_argument('--headless')
		chrome_options.add_argument('window-size=1920x1080');
		if path=="":
			path='chromedriver.exe'


		driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
		if debug:
			print(driver.capabilities)

		

	elif browser.lower()=='firefox':
		if path=="":
			path='geckodriver.exe'

		driver = webdriver.Firefox(executable_path=path)

	elif browser.lower()=='ie':
		if path=="":
			path='IEDriverServer1.exe'
		driver = webdriver.Ie(path)

	print('####################################################\n Easy selenium Library by Ankit Kothari www.step2success.in\n####################################################\n Licensed under the Apache License, Version 2.0  \n####################################################')
	return(driver)

def open_url(url='www.step2success.in',new_tab=False):
	
	if new_tab:
		driver.execute_script("window.open('{}');".format(url))
	else:
		driver.get(url)
		if debugs:
			print("Open New tab")




def found_window(name):
	def predicate(driver):
		try:
			#print('FINDING WINDOW')
			a=driver.window_handles[name]
			driver.switch_to_window(a)
			if debugs:
				print("Switch to window ",name)
		except Exception as e:
			#print ('window not found',e)
			return False
		else:
			return True # found window
	return predicate


def select_option(id,value,option):
    def predicate(driver):
        try:
            a=driver.find_element_by_xpath('//*[@{}="{}"]'.format(id,value))
            a=Select(a)
            for o in a.options:
            	if option.lower() in o.text.lower():
            		a.select_by_visible_text(o.text)
            		if debugs:
            			print("Select option",o.text)
           
        except Exception as e:
            
            return False
        else:
            return True 
    return predicate


def window_handle(no=1):
	WebDriverWait(driver, timeout=50).until(found_window(no))
	print('window handle no' ,no)


def switch_frame(no=-1,**kwargs):
	if no>=0:
		driver.switch_to.frame(no)
		if debugs:
			print("Switch to frame no",no)
		return()
	key=(list(kwargs.keys())[0])
	element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
	driver.switch_to.frame(element)
	if debugs:
			print("Switch to frame",kwargs[key])
	print('switched to frame')




def click_on(text='na',image='na',repeat_click=False,**kwargs):
	if image!='na':
		if debugs:
			print("Click on image",image)
		WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//a[img/@src="{}"]'.format(image)))).click()
		return()
	elif text!='na':
		WebDriverWait(driver,50).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text))).click()
		if debugs:
			print("Click on text",text)
		if repeat_click:
			try:
				WebDriverWait(driver,50).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text))).click()
			except:
				pass
	else:
		key=(list(kwargs.keys())[0])
		WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key])))).click()
		if debugs:
			print("click on",kwargs[key])
		if repeat_click:
			try:
				WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key])))).click()
			except:
				pass



def send_text(text,with_enter=False,**kwargs):
	key=(list(kwargs.keys())[0])
	element4 = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
	element4.send_keys(str(text))
	if debugs:
			print("Send text",text)
	if with_enter:
		element4.send_keys(Keys.ENTER)
	

def select_dropdown(option,**kwargs):
	key=(list(kwargs.keys())[0])
	WebDriverWait(driver, timeout=50).until(select_option(key,kwargs[key],option))
	print('selelct')
	

def read_text(**kwargs):
	key=(list(kwargs.keys())[0])
	element4 = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@{}="{}"]'.format(key,kwargs[key]))))
	elements4=driver.find_elements_by_xpath('//*[@{}="{}"]'.format(key,kwargs[key]))
	length=(len(elements4))
	if length>1:

		output=[]
		c=0
		
		for i in elements4:
			if i.get_attribute('value')!=None:
				output.append('("{}",{}","{}","{}")'.format(c,i.text,i.get_attribute('value'),i))
			else:
				output.append('("{}","{}","{}")'.format(c,i.text,i))
			c+=1
	else:
		if element4.get_attribute('value')!=None:
			output=(element4.text,element4.get_attribute('value'),element4)
		else:
			output=(element4.text,element4)

	if debugs:
		print('Total elements found',length)
		for j in output:
			print(j)
	return(output)



	

	return(output)

def close_window(no=0,switch_to=0):
	try:

		window_handle(no)
		driver.close()
		if debugs:
			print('close window no',no)
		if no>0:
			window_handle(switch_to)
	except:
 		print('No such window')

def alerts(text=''):

	try:
	 
	 
		 if text.lower()=='yes':
		 	driver.switch_to.alert().accept()
		 elif text.lower()=='no':
		 	driver.switch_to.alert().dismiss()
		 elif text!="":
		 	driver.switch_to.alert().send_keys(text)
		 else:
		 	a=driver.switch_to.alert().text
		 	return(a)
	except Exception as e:
		print(e,'no alert present')
	 







