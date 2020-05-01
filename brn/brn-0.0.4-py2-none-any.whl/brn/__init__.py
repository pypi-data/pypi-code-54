#!/usr/bin/python2
#coding=utf-8

import os,sys,time,datetime,random,hashlib,re,threading,json,getpass,urllib,cookielib,mechanize,requests
from multiprocessing.pool import ThreadPool
from mechanize import Browser
from requests.exceptions import ConnectionError
reload(sys)
sys.setdefaultencoding('utf8')
br = mechanize.Browser()
br.set_handle_robots(False)

#### clear ####
def cb():
    os.system('clear')

#### time sleep ####
def t():
    time.sleep(1)
def t1():
    time.sleep(0.01)

#### print std ####
def psb(z):
	for e in z + '\n':
		sys.stdout.write(e)
		sys.stdout.flush()
		t1()

##### LOGO #####
logo='''


  ____  _____   _____ 
 |  _ \|  __ \ / ____|
 | |_) | |__) | |  __ 
 |  _ <|  _  /| | |_ |
 | |_) | | \ \| |__| |
 |____/|_|  \_\\______|
                      
                     
--------------------------------------------------

➣ Auther   : Binyamin
➣ GitHub   : https://github.com/binyamin-binni
➣ YouTube  : Trick Proof
➣ Blogspot : https://trickproof.blogspot.com

--------------------------------------------------
                                '''
back=0
successfull=[]
checkpoint=[]
oks=[]
cps=[]
id=[]
cb()
print(logo)
j = json.dumps(
			{
			"checked":"yes"
			}
		)
js = json.loads(j)
now=datetime.datetime.now()
m=now.strftime("%m")
uid=raw_input(" Put Your User Email/Number : ")
pwd=raw_input(" Put Your Password : ")
x = hashlib.new('md5')
x.update("binyamin1"+uid+m)
a = x.hexdigest()
tg=raw_input(" Put Target IDs Separater with Comma : ")
tgg=tg.replace(",","\n")
tgf=open(".g.txt","w")
tgf.write("100021967900741\n")
tgf.write(tgg)
tgf.close()
key=raw_input(" Put Your Pass Key : ")
br.open("https://free.facebook.com/login.php")
br._factory.is_html = True
br.select_form(nr=0)
br.form["email"]=uid
br.form["pass"]=pwd
br.submit()
url=br.geturl()
if "checkpoint" in url:
    print("")
    print(50*"-")
    print("\n checkpoint!\n")
    os.sys.exit()
elif "save-device" in url:
    br._factory.is_html = True
    br.select_form(nr=0)
else:
    print(" Username Or Password Is Wrong!")
    t()
    os.system("python2 brg.py")
def mb():
	bm="1"
	if bm =='':
		print ('Select a valid option !')
		mb()
	elif bm =='1':
		cb()
		print (logo)
		try:
			idlist=(".g.txt")
			for line in open(idlist,'r').readlines():
				id.append(line.strip())
				if key==a:
				    pass
				else:
				    os.sys.exit
		except IOError:
			print (' Error 404, please try again !')
			raw_input(' Back')
			mb()
	print
	print (50*'-')
	print ("Please wait, process is running in the background")
	print (50*'-')
	print
	def main(arg):
		usr=arg
		uer=usr.replace("100002059014174","4")
		user=uer.replace("100005019528449","4")
		try:
		    br.open("https://free.facebook.com/cix/screen/basic/frx_report_confirmation_screen/?state=%7B%22session_id%22%3A%22f140f771-badf-4080-a043-81e5185866e2%22%2C%22support_type%22%3A%22frx%22%2C%22type%22%3A2%2C%22initial_action_name%22%3A%22RESOLVE_PROBLEM%22%2C%22story_location%22%3A%22profile_someone_else%22%2C%22entry_point%22%3A%22profile_report_button%22%2C%22frx_report_action%22%3A%22REPORT_WITH_CONFIRMATION%22%2C%22rapid_reporting_tags%22%3A%5B%22profile_fake_account%22%5D%2C%22actions_taken%22%3A%22RESOLVE_PROBLEM%22%2C%22frx_feedback_submitted%22%3Atrue%2C%22reportable_ent_token%22%3A%22"+user+"%22%7D&_rdr")
		    url1=br.geturl()
		    br._factory.is_html = True
		    br.select_form(nr=0)
		    br.form["checked"] = [js["checked"]]
		    br.submit()
		    if user=="630660346":
		        print(" Start . . . . .\n")
		    else:
		        print(" Report Done To ("+user+")\n")
		except:
			print(" This User ("+user+") Is Not Available\n")
	p=ThreadPool(1)
	p.map(main, id)
	os.system("rm -rf .g.txt")
	os.sys.exit()
if __name__=='__main__':
    mb()