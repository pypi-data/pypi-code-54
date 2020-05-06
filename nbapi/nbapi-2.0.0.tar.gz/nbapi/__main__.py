import asyncio,requests
from random import randint

#Note: Using this API you are going to be using a API that MAY (unlikely) But MAY send NSFW results.
#If that happens, DM my owner (Reine#5644), or join the Neko Support Server from the website.

#Nothing much yet :3

#                   #-------------------------------------------------#
#                       To join: Copy the below link.  
#                       https://discord.gg/RauzUYK
#                   #--------------------------------------------------#

#You may edit this code to your needs. I dont mind ;3
#TODO: make requests smaller (DONE)
class random():
    def anime():
        return f"https://reine.live/api/anime/{str(randint(int(1),int(str(requests.get('https://reine.live/api/anime/anime_c').text))))}.png"
    def neko():

                
            return f"https://reine.live/api/neko/{str(randint(int(1),int(str(requests.get('https://reine.live/api/neko/nekos_c').text))))}.png"


class search():
    def neko(num):
        return 'https://reine.live/api/neko/'+str(num)+'.png'
    def anime(num):
        return 'https://reine.live/api/anime/'+str(num)+'.png'
#print(random.pat() + random.neko() + random.anime())   #DEBUG
