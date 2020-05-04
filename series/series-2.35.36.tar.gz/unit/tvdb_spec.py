from amino.test.spec_spec import Spec
from amino import Right, Just

from golgi.test.spec import SpecConfigConcern

from series.tvdb.api import (search_show, show_by_id, season_summary, latest_season, current_episodes, airdate,
                             guess_show)
from series.tvdb.data import TvdbSeasonSummary, TvdbEpisode

sid = 71663


class TvdbSpec(SpecConfigConcern, Spec):

    def search_show(self) -> None:
        s = search_show('the_simpsons').attempt.join
        s.map(len).should.equal(Right(3))

    def show_by_id(self) -> None:
        s = show_by_id(sid).attempt.join
        s.map(lambda a: a.name).should.equal(Right('The Simpsons'))

    def summary(self) -> None:
        s = season_summary(sid).attempt.join
        s.should.equal(Right(TvdbSeasonSummary(711, 30)))

    def latest_season(self) -> None:
        s = latest_season(sid).attempt.join
        s.map(lambda e: (e.number, len(e.episodes))).should.equal(Right((30, 14)))

    def current_episodes(self) -> None:
        e = current_episodes(sid).attempt.join
        e.should.equal(Right((
            Just(TvdbEpisode(13, 30, Just(1549756800))),
            Just(TvdbEpisode(14, 30, Just(1550361600))),
        )))

    def airdate(self) -> None:
        result = airdate(sid, 30, 14).attempt.join
        result.should.equal(Right(Just(1550361600)))

    def guess_show(self) -> None:
        s = guess_show('boss').attempt.join
        s.map(lambda a: a.map(lambda b: b.name)).should.equal(Right(Just('BOSS')))


__all__ = ('TvdbSpec',)
