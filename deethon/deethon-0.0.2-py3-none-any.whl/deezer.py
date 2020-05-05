from pathlib import Path

import mutagen
import requests

from .tag import tag
from .track import Track
from .utils import blowfishDecrypt, calcbfkey, decryptfile, genurl, qualities
import deethon.constants as consts

api_link = "http://www.deezer.com/ajax/gw-light.php"


method_get_user = "deezer.getUserData"
method_get_track = "song.getData"


class Deezer:
    def __init__(self, arl_token):
        self.arl_token = arl_token
        self.req = requests.Session()
        self.req.cookies["arl"] = self.arl_token
        self.csrf_token = self.__get_api(method_get_user)["checkForm"]

    def __get_api(self, method, api_token="null", json=None):
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        return self.req.post(consts.API_LINK, params=params, json=json).json()["results"]

    def download(self, url, bitrate):
        track_id = url.split('/')[-1]
        json = {"sng_id": track_id}
        track_info = self.__get_api(method_get_track, self.csrf_token, json)
        track = Track(track_id)
        if "composer" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(composer=track_info["SNG_CONTRIBUTORS"]["composer"])
        if "author" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(author=track_info["SNG_CONTRIBUTORS"]["author"])
        
        if bitrate == "FLAC":
           bitrate = "9"
        elif bitrate == "MP3_320":
           bitrate = "3"
        elif bitrate == "MP3_256":
           bitrate = "5"
        elif bitrate == "MP3_128":
           bitrate = "1"

        ids = track_info["SNG_ID"]
        md5 = track_info["MD5_ORIGIN"]
        download_url = genurl(md5, bitrate, ids, track_info["MEDIA_VERSION"])
        crypt = self.req.get(download_url)
        if bitrate == "9":
            ext = ".flac"
        else:
            ext = ".mp3"

        std_dir = "Songs/"

        dir_path = Path(f'{std_dir}{track.album.artist}/{track.album.title}')
        dir_path.mkdir(parents=True, exist_ok=True)
        file_name = f'{track.number} - {track.title}{ext}'

        file_path = dir_path / file_name

        #output = open(file_name, "wb")

        decryptfile(crypt.iter_content(2048), calcbfkey(ids), file_path)

        #tag(file_name, track)

        return file_path
