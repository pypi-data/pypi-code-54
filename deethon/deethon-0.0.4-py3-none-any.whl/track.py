import requests


class Track:
    def __init__(self, track_id):
        r = requests.get(f"https://api.deezer.com/track/{track_id}").json()
        self.artist = r['artist']['name']
        self.bpm = r['bpm']
        self.disk_number = r['disk_number']
        self.duration = r['duration']
        self.id = r['id']
        self.isrc = r['isrc']
        self.link = r['link']
        self.number = r['track_position']
        self.replaygain_track_peak = r['gain']
        self.release_date = r['release_date']
        self.title = r['title']
        self.title_short = r['title_short']
        
        date = self.release_date.split("-") # 0 YYYY 1 MM 2 DD
        self.release_year = date[0]
        self.release_date_four_digits = f"{date[2]}{date[1]}"

        self.album_id = r['album']["id"]
        self._album = None

    @property
    def album(self) -> Album:
        if self._album:
            return self._album
        else:
            self._album = Album(self.album_id)
            return self._album

    
    def add_tags(self, **tags):
        for tag in tags:
            setattr(self, tag, tags[tag])

class Album:
    def __init__(self, album_id):
        r = requests.get(f"https://api.deezer.com/album/{album_id}").json()
        self.id = r['id']
        self.title = r['title']
        self.artist = r['artist']['name']
        self.upc = r['upc']
        self.link = r['link']
        self.record_type = r['record_type']
        self.release_date = r['release_date']
        self.total_tracks = r['nb_tracks']
        genres_list = []
        for genre in r["genres"]["data"]:
            genres_list.append(genre["name"])
        self.genres = genres_list
        self.genre = genres_list[0]
        self.label = r["label"]
        self._cover_xl = None
        self.cover_xl_url = r['cover_xl']

    @property
    def cover_xl(self):
        if self._cover_xl is None
        self._cover_xl = requests.get(self.cover_xl_url).content
        return self._cover_xl