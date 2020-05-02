class Downloader():
    def __init__(self, url):
        self.url = url

    def get_video_size(self):
        pass

    def get_video_name(self):
        pass

    def get_video_size(self):
        pass

    def download(self):
        pass

class YoutubeDownloader(Downloader):
    # we can choose many type of video
    def __init__(self, url):
        super().__init__(url)
        self.yt = YouTube(url)

    def get_video_duration(self):
        return self.yt.length

    def get_video_name(self):
        return self.yt.streams.first().default_filename

    def get_video_size(self):
        return self.yt.streams.first().filesize

    def download(self):
        #TODO: we can choose many version of video in url
        video_io = io.BytesIO()
        #for chunk in request.stream(self.yt.streams.first().url):
        #    video_io.write(chunk)
        #video_io.seek(0)
        #print(video_io.getbuffer().nbytes)
        #print(len(video_io.read()))
        self.yt.streams.first().stream_to_buffer(video_io)
        video_io.seek(0)
        #print("test" + str(len(video_io.read())))
        return video_io

class URLDownloader(Downloader):
    def __init__(self, url):
        super().__init__(url)
        req = urllib.request.Request(url, method='HEAD')
        self.r = urllib.request.urlopen(req)

    def get_video_duration(self):
        pass

    def get_video_name(self):
        return r.info().get_filename()

    def get_video_size(self):
        return r.info().getheaders("Content-Length")[0]

    def download(self):
        return io.BytesIO(self.r.read())
