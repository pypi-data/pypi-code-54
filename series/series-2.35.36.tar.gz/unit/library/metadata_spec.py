import sure  # NOQA
from flexmock import flexmock  # NOQA
from golgi import Configurations  # NOQA

from series.library import LibraryFacade
from series.library.metadata import Metadata
from series.library.model.episode import Episode
from series.library.model.series import Series
from series.library.model.season import Season

from unit._fixtures.library import create_episodes
from unit.library._support.db import DBSpec


class MetadataSpec(DBSpec):

    def setup(self, *a, **kw):
        super().setup(*a, allow_files=True, **kw)
        episodes = [
            ['2', 'series2', 3, 1, 0],
            ['2', 'series2', 3, 2, 0],
            ['1', 'series1', 5, 1, 0],
            ['1', 'series1', 5, 2, 0],
            ['1', 'series1', 5, 3, 0],
            ['1', 'series1', 6, 4, 0],
            ['1', 'series1', 6, 5, 0],
            ['1', 'series1', 6, 6, 0],
            ['1', 'series1', 6, 7, 0],
        ]
        epi_dict = dict()
        for id, ser, sea, epi, _ in episodes:
            epi_dict.setdefault(id, {}).setdefault(sea, []).append(epi)
        def etvdb(params):
            sea = int(params[3])
            season = epi_dict[params[1]][sea]
            epi = int(params[5])
            if epi == 0:
                return [self.etv_epi(sea, ep) for ep in season]
            else:
                return [self.etv_epi(sea, epi)]
        args = (a[1:] for a in episodes)
        _, self._episodes = create_episodes(['metadata'], args)
        self._lib = LibraryFacade(self._db)
        self._lib.scan()
        self._lib.episode('series1', 5, 1).new = False
        self._lib.episode('series1', 5, 3).new = False
        self._lib.episode('series2', 3, 2).new = False
        for num in range(4, 8):
            self._lib.episode('series1', 6, num).new = False
        self._meta = Metadata(self._lib, None)

    def fetch_metadata(self):
        id = "79254"
        epi = Episode(series=Series(name='miracle_workers', tvdb_id=id), season=Season(number=1), number=7)
        print(self._meta._handle_episode(epi).attempt)


__all__ = ('MetadataSpec',)
