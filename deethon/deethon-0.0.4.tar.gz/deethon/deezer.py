from pathlib import Path

import mutagen
import requests

from .constants import API_URL, METHOD_GET_DATA, METHOD_GET_USER
from .tag import tag
from .track import Track
from .utils import blowfishDecrypt, calcbfkey, decryptfile, genurl, qualities


class Deezer:
    def __init__(self, arl_token):
        self.arl_token = arl_token
        self.req = requests.Session()
        self.req.cookies["arl"] = self.arl_token
        self.csrf_token = self.__get_api(METHOD_GET_USER)["checkForm"]

    def __get_api(self, method, api_token="null", json=None):
        params = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        return self.req.post(API_URL, params=params, json=json).json()["results"]

    def __get_quality(self, bitrate: str) -> str:
        if bitrate == "FLAC":
            return "9"
        elif bitrate == "MP3_320":
            return "3"
        elif bitrate == "MP3_256":
            return "5"
        elif bitrate == "MP3_128":
            return "1"

    def download(self, url: str, bitrate: str) -> Path:
        track_id = url.split("/")[-1]
        json = {"sng_id": track_id}
        track_info = self.__get_api(METHOD_GET_DATA, self.csrf_token, json)
        track = Track(track_id)
        if "composer" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(composer=track_info["SNG_CONTRIBUTORS"]["composer"])
        if "author" in track_info["SNG_CONTRIBUTORS"].keys():
            track.add_tags(author=track_info["SNG_CONTRIBUTORS"]["author"])

        quality = self.__get_quality(bitrate)

        ids = track_info["SNG_ID"]
        md5 = track_info["MD5_ORIGIN"]
        download_url = genurl(md5, bitrate, ids, track_info["MEDIA_VERSION"])
        crypt = self.req.get(download_url)
        if bitrate == "9":
            ext = ".flac"
        else:
            ext = ".mp3"

        std_dir = "Songs/"

        dir_path = Path(f"{std_dir}{track.album.artist}/{track.album.title}")
        dir_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{track.number} - {track.title}{ext}"
        file_path = dir_path / file_name

        decryptfile(crypt.iter_content(2048), calcbfkey(ids), file_path)

        tag(file_path, track)

        return file_path
