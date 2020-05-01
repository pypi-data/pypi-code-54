# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: pymapadmin/grpc/admin.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import pymapadmin.grpc.admin_pb2


class SystemBase(abc.ABC):

    @abc.abstractmethod
    async def Ping(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.PingRequest, pymapadmin.grpc.admin_pb2.PingResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/admin.System/Ping': grpclib.const.Handler(
                self.Ping,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.admin_pb2.PingRequest,
                pymapadmin.grpc.admin_pb2.PingResponse,
            ),
        }


class SystemStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Ping = grpclib.client.UnaryUnaryMethod(
            channel,
            '/admin.System/Ping',
            pymapadmin.grpc.admin_pb2.PingRequest,
            pymapadmin.grpc.admin_pb2.PingResponse,
        )


class MailboxBase(abc.ABC):

    @abc.abstractmethod
    async def Append(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.AppendRequest, pymapadmin.grpc.admin_pb2.AppendResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/admin.Mailbox/Append': grpclib.const.Handler(
                self.Append,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.admin_pb2.AppendRequest,
                pymapadmin.grpc.admin_pb2.AppendResponse,
            ),
        }


class MailboxStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Append = grpclib.client.UnaryUnaryMethod(
            channel,
            '/admin.Mailbox/Append',
            pymapadmin.grpc.admin_pb2.AppendRequest,
            pymapadmin.grpc.admin_pb2.AppendResponse,
        )


class UserBase(abc.ABC):

    @abc.abstractmethod
    async def ListUsers(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.ListUsersRequest, pymapadmin.grpc.admin_pb2.ListUsersResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GetUser(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.GetUserRequest, pymapadmin.grpc.admin_pb2.UserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SetUser(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.SetUserRequest, pymapadmin.grpc.admin_pb2.UserResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DeleteUser(self, stream: 'grpclib.server.Stream[pymapadmin.grpc.admin_pb2.DeleteUserRequest, pymapadmin.grpc.admin_pb2.UserResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/admin.User/ListUsers': grpclib.const.Handler(
                self.ListUsers,
                grpclib.const.Cardinality.UNARY_STREAM,
                pymapadmin.grpc.admin_pb2.ListUsersRequest,
                pymapadmin.grpc.admin_pb2.ListUsersResponse,
            ),
            '/admin.User/GetUser': grpclib.const.Handler(
                self.GetUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.admin_pb2.GetUserRequest,
                pymapadmin.grpc.admin_pb2.UserResponse,
            ),
            '/admin.User/SetUser': grpclib.const.Handler(
                self.SetUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.admin_pb2.SetUserRequest,
                pymapadmin.grpc.admin_pb2.UserResponse,
            ),
            '/admin.User/DeleteUser': grpclib.const.Handler(
                self.DeleteUser,
                grpclib.const.Cardinality.UNARY_UNARY,
                pymapadmin.grpc.admin_pb2.DeleteUserRequest,
                pymapadmin.grpc.admin_pb2.UserResponse,
            ),
        }


class UserStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.ListUsers = grpclib.client.UnaryStreamMethod(
            channel,
            '/admin.User/ListUsers',
            pymapadmin.grpc.admin_pb2.ListUsersRequest,
            pymapadmin.grpc.admin_pb2.ListUsersResponse,
        )
        self.GetUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/admin.User/GetUser',
            pymapadmin.grpc.admin_pb2.GetUserRequest,
            pymapadmin.grpc.admin_pb2.UserResponse,
        )
        self.SetUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/admin.User/SetUser',
            pymapadmin.grpc.admin_pb2.SetUserRequest,
            pymapadmin.grpc.admin_pb2.UserResponse,
        )
        self.DeleteUser = grpclib.client.UnaryUnaryMethod(
            channel,
            '/admin.User/DeleteUser',
            pymapadmin.grpc.admin_pb2.DeleteUserRequest,
            pymapadmin.grpc.admin_pb2.UserResponse,
        )
