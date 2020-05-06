from typing import NoReturn

from pyquire.api import api
from pyquire.models.board.board import Board, Boards
from pyquire.models.board.create_board_body import CreateBoardBody
from pyquire.models.board.update_board_body import UpdateBoardBody
from pyquire.models.common import OID, ID

__all__ = ["BoardResource"]


@api.path("/board")
class BoardResource:

    @api.post
    @api.path("/{project_oid}")
    def create_board(self, *, project_oid: OID, data: CreateBoardBody) -> Board:
        """Add a new board.

        Add a new board into a project.

        Args:
            project_oid (:obj:`str`): OID of project that this new board to be added to.
            data (:obj:`models.board.create_board_body.CreateBoardBody`): Board to create.

        Returns:
            :obj:`models.board.board.Board`: Board.
        """
        pass

    @api.post
    @api.path("/id/{project_id}")
    def create_board_to_project(self, *, project_id: ID, data: CreateBoardBody) -> Board:
        """Add a new board.

        Add a new board into a project.

        Args:
            project_id (:obj:`str`): ID of project that this new board to be added to.
            data (:obj:`models.board.create_board_body.CreateBoardBody`): Board to create.

        Returns:
            :obj:`models.board.board.Board`: Board.
        """
        pass

    @api.get
    @api.path("/{oid}")
    def get_board(self, *, oid: OID) -> Board:
        """Get an existing board by its OID

        Returns the full board record of the given OID.

        Args:
            oid (:obj:`str`): OID of board that needs to be fetched.

        Returns:
            :obj:`models.board.board.Board`: Board.
        """
        pass

    @api.get
    @api.path("/id/{project_id}/{id}")
    def get_board_by_id(self, *, project_id: ID, id: ID) -> Board:
        """Get an existing board by its ID.

        Returns the full board record of the given ID.

        Args:
            project_id (:obj:`str`): ID of the project that the board belongs to.
            id (:obj:`str`): ID of the board that needs to be fetched.

        Returns:
            :obj:`models.board.board.Board`: Board.
        """
        pass

    @api.get
    @api.path("/list/{project_oid}")
    def get_boards_by_project_oid(self, *, project_oid: OID) -> Boards:
        """Get all boards of the given project by its OID.

        Returns all board records of the given project by its OID.

        Args:
            project_oid (:obj:`str`): OID of the project.

        Returns:
            :obj:`list` of :obj:`models.board.board.Board`: Boards.
        """
        pass

    @api.get
    @api.path("/list/id/{project_id}")
    def get_boards_by_project_id(self, *, project_id: ID) -> Boards:
        """Get all boards of the given project by its ID.

        Returns all board records of the given project by its ID.

        Args:
            project_id (:obj:`str`): ID of project.

        Returns:
            :obj:`list` of :obj:`models.board.board.Board`: Boards.
        """
        pass

    @api.put
    @api.path("/{oid}")
    def update_board(self, *, oid: OID, data: UpdateBoardBody) -> Board:
        """Update a board.

        Updates an existing board, and returns the complete updated record.

        Args:
            oid (:obj:`str`): OID of board that needs to be updated
            data (:obj:``): Board to update.

        Returns:
            :obj:`models.board.board.Board`: Updated board.
        """
        pass

    @api.delete
    @api.path("/{oid}")
    def delete_board(self, *, oid: OID) -> NoReturn:
        """Delete a board

        Delete an existing board of the given OID.

        Args:
            oid (:obj:`str`): OID of board that needs to be deleted
        """
        pass
