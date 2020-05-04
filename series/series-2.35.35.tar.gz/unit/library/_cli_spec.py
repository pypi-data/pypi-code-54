import shutil
import time
import os
import threading

from golgi import Config
from amino.test import temp_dir

from series.library import SeriesLibraryD
from series.library.client.rest_api import LibClient
from series.library.model.series import Series
from series.library.model.season import Season
from series.library.model.episode import Episode

from unit.library._support.spec import Spec


class _CLI(Spec):

    def setup(self, *a, **kw):
        super().setup(*a, **kw)

    def run_the_daemon(self):
        lib_dir = temp_dir('library', 'cli')
        shutil.copy(os.path.expanduser('~/.local/share/series/library.db'), str(lib_dir))
        Config.override('library', db_path=lib_dir / 'library.db', rest_api_port=8112)
        Config.override('library_client', rest_api_url='http://localhost', rest_api_port=8112)
        Config.override('player', player_type='mpv')
        daemon = SeriesLibraryD()
        daemon.rest_api.app.config['TESTING'] = True
        client = LibClient()
        # episode = daemon.metadata._library.episode('the_simpsons', 30, 12)
        # episode.overview = 'asdf'
        # episode = daemon.metadata._library.episode('the_simpsons', 30, 12)
        # daemon.metadata._handle(episode)
        # episode = daemon.metadata._library.episode('the_simpsons', 30, 12).overview
        thread = threading.Thread(target=daemon.run)
        thread.start()
        time.sleep(.5)
        db = daemon.rest_api._library._db
        def epi(name, e) -> None:
            s = db.query(Series).filter_by(name='the_simpsons').first()
            return s.seasons.filter(Season.number == name).first().episodes.filter(Episode.number == e).first()
        time.sleep(.5)
        print(client.mark_episode_new('the_simpsons', '28-30'))
        time.sleep(.5)
        print(epi(30, 1).new)
        daemon.interrupt()

__all__ = ('_CLI',)
