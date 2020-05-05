import os
import pickle

from .data_update import DataUpdate


class Papers(list):
    """
    This class is responsible for downloading and containing the papers.
    """

    CACHE_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/cache.pickle"

    def __init__(self, force_refresh: bool = False) -> None:
        """
        The constructor for the Papers class.

        :param force_refresh: (bool) forces a fresh download.
        """
        super().__init__([])
        if self.cache_exists is True and force_refresh is False:
            self._load()
        else:
            self._get_data()
            self._save()

    def _get_data(self) -> None:
        """
        Updates self with data from source.

        :return: None
        """
        print("Getting data from source...")
        data_getter = DataUpdate()
        data_getter.get_data()

        for paper in data_getter.data:
            self.append(paper)
        print("data collected")

    def _save(self) -> None:
        """
        Saves the object as a pickle file.

        :return: None
        """
        with open(self.CACHE_PATH, 'wb') as handle:
            pickle.dump(self, handle)

    def _load(self) -> None:
        """
        Loads the object from a pickle file.

        :return: None
        """
        print("loading from cache...")
        with open(self.CACHE_PATH, 'rb') as handle:
            data = pickle.load(handle)
            for i in data:
                self.append(i)
        print("data loaded")

    @property
    def cache_exists(self) -> bool:
        """
        Checks to see if cache exists.

        :return: True if so => False if not
        """
        if os.path.exists(self.CACHE_PATH):
            return True
        return False
