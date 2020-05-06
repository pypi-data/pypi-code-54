__version__ = '0.1.1'

import logging

log = logging.getLogger(__name__)


class SubUid(object):
    def __init__(self, name, start, count):
        self.name = name
        self.start = int(start)
        self.count = int(count)

    @property
    def end(self):
        return self.start + self.count - 1

    def __str__(self):
        return '%s:%s:%s' % (self.name, self.start, self.count)

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.end

    def verify(self, other):
        '''Check to see if we overlap with another SubUid class'''
        if self.start < other.start:
            if self.end < other.start:
                return True
            else:
                log.warning('Overlap error: %s end is > %s start'
                            % (self, other))
        else:
            log.warning('Sorting error: %s start is > %s start'
                        % (self, other))
        return False


class SubUidList(object):
    def __init__(self, minid=100000):
        self._list = []
        # We set a minimum floor in the IDs we would allowed to be allocated
        self.minid = int(minid)

    def allocate(self, name, start=None, count=None):
        self._list.sort()
        if len(self._list) == 0:
            s = start or 4294000000
            c = count or 100000
        else:
            s = start or self._list[0].start - self._list[0].count
            c = count or self._list[0].count
        if int(s) < self.minid:
            # we are trying to allocate a subuid under our floor
            return False
        subuid = SubUid(name=name, start=s, count=c)
        self.append(subuid)
        if self.verify():
            return True
        else:
            log.error('Falied to allocate subuid %s' % (subuid))
            self.remove(subuid)
            return False

    def append(self, subuid):
        if type(subuid) is not SubUid:
            raise TypeError
        self._list.append(subuid)
        self._list.sort()

    def remove(self, subuid):
        self._list.remove(subuid)

    def __repr__(self):
        if len(self._list) > 0:
            return ', '.join([x.__repr__() for x in self._list])
        else:
            return '[]'

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        self.n = 0
        self._list.sort()
        return self

    def __next__(self):
        if self.n < len(self._list):
            next = self._list[self.n]
            self.n += 1
            return next
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def name_in(self, name):
        return name in [x.name for x in self._list]

    def verify(self):
        self._list.sort()
        for i in range(len(self._list)-1):
            if self._list[i].verify(self._list[i+1]):
                continue
            else:
                return False
        if len(set([x.name for x in self._list])) != len(self._list):
            log.error('Duplicate users in list.')
            return False
        return True
