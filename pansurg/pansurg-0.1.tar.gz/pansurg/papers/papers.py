from .data_update import DataUpdate


class Papers(list):
    """
    This class is responsible for downloading and containing the papers.
    """
    def __init__(self) -> None:
        """
        The constructor for the Papers class.
        """
        super().__init__([])
        self._get_data()

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
