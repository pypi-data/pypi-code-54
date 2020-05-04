import time
import webbrowser as web
import wikipedia
import requests
from bs4 import BeautifulSoup
import urllib.request
import speedtest

check=bool()

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
    except:
        raise Exception("You are not connect to internet")

def authour_name(a):
    if a == "256832":
        return "Badal Shrivastav and Shambhavi Lal"
    return "Void"

def check_internet_speed():
    print("Wait...")
    test=speedtest.Speedtest()
    return "Download Speed {} bit/s \nUpload Speed {}bit/s".format(int(test.download()),int(test.upload()))


def send_message(mobile_no, message, hour, minute):
    '''Reminds you to send message on whatsapp using your whatsapp web so please connect your laptop with whatsapp web'''
    if hour == 0:
        hour = 24
    second = (hour * 3600) + (min * 60)

    now = time.localtime()
    h = now.tm_hour
    m = now.tm_min
    s = now.tm_sec

    current_sec = (h * 3600) + (m * 60) + (s)
    remaining = second - current_sec

    if remaining <= 0:
        remaining = 86400 + remaining

    if remaining < 60:
        raise Exception("Message time should be after 2 min")

    else:
        sleep_time = remaining - 60
        time.sleep(sleep_time)
        web.open('https://web.whatsapp.com/send?phone=' + mobile_no + '&text=' + message)
        time.sleep(2)


def info(subject, lines=3, speak=None):
    '''Gives information on the topic'''
    var= wikipedia.summary(subject, sentences=lines)
    return var


def play_youtube(title):
    '''Play video on youtube that you entered'''
    url = 'https://www.youtube.com/results?q=' + title
    url_details= requests.get(url)
    text = url_details.text
    soup = BeautifulSoup(text, "html.parser")
    video = soup.findAll("div", {"class": "yt-lockup-video"})
    video= video[0].contents[0].contents[0].contents[0]
    web.open("https://www.youtube.com" + video["href"])


def search(subject):
    '''Searches about the topic on Google'''
    search= 'https://www.google.com/search?q={}'.format(subject)
    web.open(search)

connect()
