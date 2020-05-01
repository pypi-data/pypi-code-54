#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekokatt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Single-threaded asyncio Gateway implementation.

Handles regular heartbeating in a background task
on the same event loop. Implements zlib transport compression only.

Can be used as the main gateway connection for a single-sharded bot, or the gateway connection for a
specific shard in a swarm of shards making up a larger bot.

References
----------
* [IANA WS closure code standards](https://www.iana.org/assignments/websocket/websocket.xhtml)
* [Gateway documentation](https://discordapp.com/developers/docs/topics/gateway)
* [Opcode documentation](https://discordapp.com/developers/docs/topics/opcodes-and-status-codes)
"""

from __future__ import annotations

__all__ = ["Shard"]

import asyncio
import contextlib
import datetime
import json
import logging
import math
import time
import typing
import urllib.parse
import zlib

import aiohttp.typedefs

from hikari import errors
from hikari.internal import more_asyncio
from hikari.net import codes
from hikari.net import ratelimits
from hikari.net import user_agents

if typing.TYPE_CHECKING:
    import ssl

    from hikari import intents as _intents


DispatchT = typing.Callable[["Shard", str, typing.Dict], None]
"""The signature for an event dispatch callback."""


VERSION_6: typing.Final[int] = 6
VERSION_7: typing.Final[int] = 7


class Shard:  # pylint: disable=too-many-instance-attributes
    """Implementation of a client for the Discord Gateway.

    This is a websocket connection to Discord that is used to inform your
    application of events that occur, and to allow you to change your presence,
    amongst other real-time applications.

    Each `Shard` represents a single shard.

    Expected events that may be passed to the event dispatcher are documented in the
    [gateway event reference](https://discordapp.com/developers/docs/topics/gateway#commands-and-events) .
    No normalization of the gateway event names occurs. In addition to this,
    some internal events can also be triggered to notify you of changes to
    the connection state.

    * `CONNECTED` - fired on initial connection to Discord.
    * `DISCONNECTED` - fired when the connection is closed for any reason.

    Parameters
    ----------
    compression : bool
        If `True`, then payload compression is enabled on the connection.
        If `False`, no payloads are compressed. You usually want to keep this
        enabled.
    connector : aiohttp.BaseConnector, optional
        The `aiohttp.BaseConnector` to use for the HTTP session that
        gets upgraded to a websocket connection. You can use this to customise
        connection pooling, etc.
    debug : bool
        If `True`, the client is configured to provide extra contextual
        information to use when debugging this library or extending it. This
        includes logging every payload that is sent or received to the logger
        as debug entries. Generally it is best to keep this disabled.
    dispatch : `dispatch function`
        The function to invoke with any dispatched events. This must not be a
        coroutine function, and must take three arguments only. The first is
        the reference to this `Shard` The second is the
        event name.
    initial_presence : typing.Dict, optional
        A raw JSON object as a `typing.Dict` that should be set as the
        initial presence of the bot user once online. If `None`, then it
        will be set to the default, which is showing up as online without a
        custom status message.
    intents : hikari.intents.Intent, optional
        Bitfield of intents to use. If you use the V7 API, this is mandatory.
        This field will determine what events you will receive.
    json_deserialize : `deserialization function`
        A custom JSON deserializer function to use. Defaults to `json.loads`.
    json_serialize : `serialization function`
        A custom JSON serializer function to use. Defaults to `json.dumps`.
    large_threshold : int
        The number of members that have to be in a guild for it to be
        considered to be "large". Large guilds will not have member information
        sent automatically, and must manually request that member chunks be
        sent using `ShardConnection.request_guild_members`.
    proxy_auth : aiohttp.BasicAuth, optional
        Optional `aiohttp.BasicAuth` object that can be provided to
        allow authenticating with a proxy if you use one. Leave `None` to ignore.
    proxy_headers : typing.Mapping[str, str], optional
        Optional `typing.Mapping` to provide as headers to allow the
        connection through a proxy if you use one. Leave `None` to ignore.
    proxy_url : str, optional
        Optional `str` to use for a proxy server. If `None`, then it is ignored.
    session_id : str, optional
        The session ID to use. If specified along with `seq`, then the
        gateway client will attempt to `RESUME` an existing session rather than
        re-`IDENTIFY`. Otherwise, it will be ignored.
    seq : int, optional
        The sequence number to use. If specified along with `session_id`, then
        the gateway client will attempt to `RESUME` an existing session rather
        than re-`IDENTIFY`. Otherwise, it will be ignored.
    shard_id : int
        The shard ID of this gateway client. Defaults to `0`.
    shard_count : int
        The number of shards on this gateway. Defaults to `1`, which implies no
        sharding is taking place.
    ssl_context : ssl.SSLContext, optional
        An optional custom `ssl.SSLContext` to provide to customise how
        SSL works.
    token : str
        The mandatory bot token for the bot account to use, minus the "Bot"
        authentication prefix used elsewhere.
    url : str
        The websocket URL to use.
    verify_ssl : bool
        If `True`, SSL verification is enabled, which is generally what you
        want. If you get SSL issues, you can try turning this off at your own
        risk.
    version : int
        The version of the API to use. Defaults to the most recent stable
        version (v6).
    """

    __slots__ = (
        "_compression",
        "_connected_at",
        "_connector",
        "_debug",
        "_intents",
        "_json_deserialize",
        "_json_serialize",
        "_large_threshold",
        "_presence",
        "_proxy_auth",
        "_proxy_headers",
        "_proxy_url",
        "_ratelimiter",
        "_session",
        "_ssl_context",
        "_token",
        "_url",
        "_verify_ssl",
        "_ws",
        "_zlib",
        "closed_event",
        "disconnect_count",
        "dispatch",
        "handshake_event",
        "heartbeat_interval",
        "heartbeat_latency",
        "hello_event",
        "last_heartbeat_sent",
        "last_message_received",
        "logger",
        "ready_event",
        "requesting_close_event",
        "resumed_event",
        "seq",
        "session_id",
        "shard_count",
        "shard_id",
        "status",
        "version",
    )

    _compression: bool
    _connected_at: float
    _connector: typing.Optional[aiohttp.BaseConnector]
    _debug: bool
    _intents: typing.Optional[_intents.Intent]
    _large_threshold: int
    _json_deserialize: typing.Callable[[typing.AnyStr], typing.Dict]
    _json_serialize: typing.Callable[[typing.Dict], typing.AnyStr]
    _presence: typing.Optional[typing.Dict]
    _proxy_auth: typing.Optional[aiohttp.BasicAuth]
    _proxy_headers: typing.Optional[aiohttp.typedefs.LooseHeaders]
    _proxy_url: typing.Optional[str]
    _ratelimiter: ratelimits.WindowedBurstRateLimiter
    _session: typing.Optional[aiohttp.ClientSession]
    _ssl_context: typing.Optional[ssl.SSLContext]
    _token: str
    _url: str
    _verify_ssl: bool
    _ws: typing.Optional[aiohttp.ClientWebSocketResponse]
    _zlib: typing.Optional[zlib.decompressobj]

    closed_event: typing.Final[asyncio.Event]
    """An event that is set when the connection closes."""

    disconnect_count: int
    """The number of times we have disconnected from the gateway on this
    client instance.
    """

    dispatch: DispatchT
    """The dispatch method to call when dispatching a new event.

    This is the method passed in the constructor.
    """

    heartbeat_interval: float
    """The heartbeat interval Discord instructed the client to beat at.

    This is `nan` until this information is received.
    """

    heartbeat_latency: float
    """The most recent heartbeat latency measurement in seconds.

    This is `nan` until this information is available. The latency is calculated
    as the time between sending a `HEARTBEAT` payload and receiving a
    `HEARTBEAT_ACK` response.
    """

    hello_event: typing.Final[asyncio.Event]
    """An event that is set when Discord sends a `HELLO` payload.

    This indicates some sort of connection has successfully been made.
    """

    handshake_event: typing.Final[asyncio.Event]
    """An event that is set when the client has successfully `IDENTIFY`ed
    or `RESUMED` with the gateway.

    This indicates regular communication can now take place on the connection
    and events can be expected to be received.
    """

    last_heartbeat_sent: float
    """The monotonic timestamp that the last `HEARTBEAT` was sent at.

    This will be `nan` if no `HEARTBEAT` has yet been sent.
    """

    last_message_received: float
    """The monotonic timestamp at which the last payload was received from Discord.

    If this was more than the `heartbeat_interval` from the current time, then
    the connection is assumed to be zombied and is shut down.
    If no messages have been received yet, this is `nan`.
    """

    logger: typing.Final[logging.Logger]
    """The logger used for dumping information about what this client is doing."""

    ready_event: typing.Final[asyncio.Event]
    """An event that is triggered when a `READY` payload is received for the shard.

    This indicates that it successfully started up and had a correct sharding
    configuration. This is more appropriate to wait for than
    `Shard.handshake_event` since the former will still fire if starting
    shards too closely together, for example. This would still lead to an
    immediate invalid session being fired afterwards.

    It is worth noting that this event is only set for the first `READY` event
    after connecting with a fresh connection. For all other purposes, you should
    wait for the event to be fired in the `dispatch` function you provide.
    """

    resumed_event: typing.Final[asyncio.Event]
    """An event that is triggered when a resume has succeeded on the gateway."""

    requesting_close_event: typing.Final[asyncio.Event]
    """An event that is set when something requests that the connection should
    close somewhere.
    """

    session_id: typing.Optional[str]
    """The current session ID, if known."""

    seq: typing.Optional[int]
    """The current sequence number for state synchronization with the API,
    if known.
    """

    shard_id: typing.Final[int]
    """The shard ID."""

    shard_count: typing.Final[int]
    """The number of shards in use for the bot."""

    version: typing.Final[int]
    """The API version to use on Discord."""

    def __init__(  # pylint: disable=too-many-locals
        self,
        *,
        compression: bool = True,
        connector: typing.Optional[aiohttp.BaseConnector] = None,
        debug: bool = False,
        dispatch: DispatchT = lambda gw, e, p: None,
        initial_presence: typing.Optional[typing.Dict] = None,
        intents: typing.Optional[_intents.Intent] = None,
        json_deserialize: typing.Callable[[typing.AnyStr], typing.Dict] = json.loads,
        json_serialize: typing.Callable[[typing.Dict], typing.AnyStr] = json.dumps,
        large_threshold: int = 250,
        proxy_auth: typing.Optional[aiohttp.BasicAuth] = None,
        proxy_headers: typing.Optional[aiohttp.typedefs.LooseHeaders] = None,
        proxy_url: typing.Optional[str] = None,
        session_id: typing.Optional[str] = None,
        seq: typing.Optional[int] = None,
        shard_id: int = 0,
        shard_count: int = 1,
        ssl_context: typing.Optional[ssl.SSLContext] = None,
        token: str,
        url: str,
        verify_ssl: bool = True,
        version: int = VERSION_6,
    ) -> None:
        # Sanitise the URL...
        scheme, netloc, path, params, _, _ = urllib.parse.urlparse(url, allow_fragments=True)

        new_query = dict(v=int(version), encoding="json")
        if compression:
            # payload compression
            new_query["compress"] = "zlib-stream"

        new_query = urllib.parse.urlencode(new_query)

        url = urllib.parse.urlunparse((scheme, netloc, path, params, new_query, ""))

        self._compression = compression
        self._connected_at = float("nan")
        self._connector = connector
        self._debug = debug
        self._intents = intents
        self._large_threshold = large_threshold
        self._json_deserialize = json_deserialize
        self._json_serialize = json_serialize
        self._presence = initial_presence
        self._proxy_auth = proxy_auth
        self._proxy_headers = proxy_headers
        self._proxy_url = proxy_url
        self._ratelimiter = ratelimits.WindowedBurstRateLimiter(str(shard_id), 60.0, 120)
        self._session: typing.Optional[aiohttp.ClientSession] = None
        self._ssl_context: typing.Optional[ssl.SSLContext] = ssl_context
        self._token = token
        self._url = url
        self._verify_ssl = verify_ssl
        self._ws = None
        self._zlib = None
        self.closed_event = asyncio.Event()
        self.disconnect_count = 0
        self.dispatch = dispatch
        self.heartbeat_interval = float("nan")
        self.heartbeat_latency = float("nan")
        self.hello_event = asyncio.Event()
        self.handshake_event = asyncio.Event()
        self.last_heartbeat_sent = float("nan")
        self.last_message_received = float("nan")
        self.logger = logging.getLogger(f"hikari.net.{type(self).__qualname__}.{shard_id}")
        self.requesting_close_event = asyncio.Event()
        self.ready_event = asyncio.Event()
        self.resumed_event = asyncio.Event()
        self.session_id = session_id
        self.seq = seq
        self.shard_id = shard_id
        self.shard_count = shard_count
        self.version = version

    @property
    def uptime(self) -> datetime.timedelta:
        """Amount of time the connection has been running for.

        If this connection isn't running, this will always be `0` seconds.
        """
        delta = time.perf_counter() - self._connected_at
        return datetime.timedelta(seconds=0 if math.isnan(delta) else delta)

    @property
    def is_connected(self) -> bool:
        """Whether the gateway is connected or not."""
        return not math.isnan(self._connected_at)

    @property
    def intents(self) -> typing.Optional[_intents.Intent]:
        """Intents being used.

        If this is `None`, no intent usage was being used on this shard.
        On V6 this would be regular usage as prior to the intents change in
        January 2020. If on V7, you just won't be able to connect at all to the
        gateway.
        """
        return self._intents

    @property
    def reconnect_count(self) -> int:
        """Amount of times the gateway has reconnected since initialization.

        This can be used as a debugging context, but is also used internally
        for exception management.
        """
        # 0 disconnects + not is_connected => 0
        # 0 disconnects + is_connected => 0
        # 1 disconnects + not is_connected = 0
        # 1 disconnects + is_connected = 1
        # 2 disconnects + not is_connected = 1
        # 2 disconnects + is_connected = 2
        return max(0, self.disconnect_count - int(not self.is_connected))

    # Ignore docstring not starting in an imperative mood
    @property
    def current_presence(self) -> typing.Dict:  # noqa: D401
        """Current presence for the gateway."""
        # Make a shallow copy to prevent mutation.
        return dict(self._presence or {})

    @typing.overload
    async def request_guild_members(self, guild_id: str, *guild_ids: str, limit: int = 0, query: str = "") -> None:
        """Request guild members in the given guilds using a query string and an optional limit."""

    @typing.overload
    async def request_guild_members(self, guild_id: str, *guild_ids: str, user_ids: typing.Sequence[str]) -> None:
        """Request guild members in the given guilds using a set of user IDs to resolve."""

    async def request_guild_members(self, guild_id, *guild_ids, **kwargs):
        """Request the guild members for a guild or set of guilds.

        These guilds must be being served by this shard, and the results will be
        provided to the dispatcher with `GUILD_MEMBER_CHUNK` events.

        Parameters
        ----------
        guild_id : str
            The first guild to request members for.
        *guild_ids : str
            Additional guilds to request members for.
        **kwargs
            Optional arguments.

        Keyword Args
        ------------
        limit : int
            Limit for the number of members to respond with. Set to `0` to be
            unlimited.
        query : str
            An optional string to filter members with. If specified, only
            members who have a username starting with this string will be
            returned.
        user_ids : typing.Sequence[str]
            An optional list of user IDs to return member info about.

        !!! note
            You may not specify `user_id` at the same time as `limit` and
            `query`. Likewise, if you specify one of `limit` or `query`, the
            other must also be included. The default, if no optional arguments
            are specified, is to use a `limit = 0` and a `query = ""`
            (empty-string).
        """
        guilds = [guild_id, *guild_ids]
        constraints = {}

        if "presences" in kwargs:
            constraints["presences"] = kwargs["presences"]

        if "user_ids" in kwargs:
            constraints["user_ids"] = kwargs["user_ids"]
        else:
            constraints["query"] = kwargs.get("query", "")
            constraints["limit"] = kwargs.get("limit", 0)

        self.logger.debug(
            "requesting guild members for guilds %s with constraints %s", guilds, constraints,
        )

        await self._send({"op": codes.GatewayOpcode.REQUEST_GUILD_MEMBERS, "d": {"guild_id": guilds, **constraints}})

    async def update_presence(self, presence: typing.Dict) -> None:
        """Change the presence of the bot user for this shard.

        Parameters
        ----------
        presence : typing.Dict
            The new presence payload to set.
        """
        presence.setdefault("since", None)
        presence.setdefault("game", None)
        presence.setdefault("status", "online")
        presence.setdefault("afk", False)

        self.logger.debug("updating presence to %r", presence)
        await self._send({"op": codes.GatewayOpcode.PRESENCE_UPDATE, "d": presence})
        self._presence = presence

    async def connect(self, client_session_type=aiohttp.ClientSession) -> None:
        """Connect to the gateway and return when it closes.

        Parameters
        ----------
        client_session_type : aiohttp.ClientSession
            The client session implementation to use. You generally do not want
            to change this from the default, which is `aiohttp.ClientSession`.
        """
        if self.is_connected:
            raise RuntimeError("Already connected")

        self.closed_event.clear()
        self.hello_event.clear()
        self.handshake_event.clear()
        self.ready_event.clear()
        self.requesting_close_event.clear()
        self.resumed_event.clear()

        self._session = client_session_type(**self._cs_init_kwargs())

        # 1000 and 1001 will invalidate sessions, 1006 (used here before)
        # is a sketchy area as to the intent. 4000 is known to work normally.
        close_code = codes.GatewayCloseCode.UNKNOWN_ERROR

        try:
            self._ws = await self._session.ws_connect(**self._ws_connect_kwargs())
            self._zlib = zlib.decompressobj()
            self.logger.debug("expecting HELLO")
            pl = await self._receive()

            self._connected_at = time.perf_counter()

            op = pl["op"]
            if op != 10:
                raise errors.GatewayError(f"Expected HELLO opcode 10 but received {op}")

            self.heartbeat_interval = pl["d"]["heartbeat_interval"] / 1_000.0

            self.hello_event.set()

            self.dispatch(self, "CONNECTED", {})
            self.logger.debug("received HELLO (interval:%ss)", self.heartbeat_interval)

            completed, pending_tasks = await more_asyncio.wait(
                [self._heartbeat_keep_alive(self.heartbeat_interval), self._run()], return_when=asyncio.FIRST_COMPLETED,
            )

            # Kill other running tasks now.
            for pending_task in pending_tasks:
                pending_task.cancel()
                with contextlib.suppress(Exception):
                    # Clear any pending exception to prevent a nasty console message.
                    pending_task.result()

            # If the heartbeat call closes normally, then we want to get the exception
            # raised by the identify call if it raises anything. This prevents spammy
            # exceptions being thrown if the client shuts down during the handshake,
            # which becomes more and more likely when we consider bots may have many
            # shards running, each taking min of 5s to start up after the first.
            ex = None
            while len(completed) > 0 and ex is None:
                ex = completed.pop().exception()

            if ex is None:
                # If no exception occurred, we must have exited non-exceptionally, indicating
                # the close event was set without an error causing that flag to be changed.
                ex = errors.GatewayClientClosedError()
                close_code = codes.GatewayCloseCode.NORMAL_CLOSURE

            elif isinstance(ex, asyncio.TimeoutError):
                # If we get timeout errors receiving stuff, propagate as a zombied connection. This
                # is already done by the ping keepalive and heartbeat keepalive partially, but this
                # is a second edge case.
                ex = errors.GatewayZombiedError()

            if hasattr(ex, "close_code"):
                close_code = ex.close_code

            raise ex

        finally:
            self.closed_event.set()

            if not math.isnan(self._connected_at):
                await self.close(close_code)
                self.dispatch(self, "DISCONNECTED", {})
                self.disconnect_count += 1

            self._ws = None

            self._connected_at = float("nan")
            self.last_heartbeat_sent = float("nan")
            self.heartbeat_latency = float("nan")
            self.last_message_received = float("nan")

            await self._session.close()
            self._session = None

    async def close(self, close_code: int = 1000) -> None:
        """Request this gateway connection closes.

        Parameters
        ----------
        close_code : int
            The close code to use. Defaults to `1000` (normal closure).
        """
        if not self.requesting_close_event.is_set():
            self.logger.debug("closing websocket connection")
            self.requesting_close_event.set()
            # These will attribute error if they are not set; in this case we don't care, just ignore it.
            with contextlib.suppress(asyncio.TimeoutError, AttributeError):
                await asyncio.wait_for(self._ws.close(code=close_code), timeout=2.0)
            with contextlib.suppress(asyncio.TimeoutError, AttributeError):
                await asyncio.wait_for(self._session.close(), timeout=2.0)
            self.closed_event.set()
        elif self._debug:
            self.logger.debug("websocket connection already requested to be closed, will not do anything else")

    def _ws_connect_kwargs(self):
        return dict(
            url=self._url,
            compress=0,
            autoping=True,
            max_msg_size=0,
            proxy=self._proxy_url,
            proxy_auth=self._proxy_auth,
            proxy_headers=self._proxy_headers,
            verify_ssl=self._verify_ssl,
            ssl_context=self._ssl_context,
        )

    def _cs_init_kwargs(self):
        return dict(connector=self._connector)

    async def _heartbeat_keep_alive(self, heartbeat_interval):
        while not self.requesting_close_event.is_set():
            self._zombie_detector(heartbeat_interval)
            self.logger.debug("preparing to send HEARTBEAT (s:%s, interval:%ss)", self.seq, self.heartbeat_interval)
            await self._send({"op": codes.GatewayOpcode.HEARTBEAT, "d": self.seq})
            self.last_heartbeat_sent = time.perf_counter()

            try:
                await asyncio.wait_for(self.requesting_close_event.wait(), timeout=heartbeat_interval)
            except asyncio.TimeoutError:
                pass

    def _zombie_detector(self, heartbeat_interval):
        time_since_message = time.perf_counter() - self.last_message_received
        if heartbeat_interval < time_since_message:
            raise asyncio.TimeoutError(
                f"{self.shard_id}: connection is a zombie, haven't received any message for {time_since_message}s"
            )

    async def _identify(self):
        self.logger.debug("preparing to send IDENTIFY")

        # noinspection PyArgumentList
        pl = {
            "op": codes.GatewayOpcode.IDENTIFY,
            "d": {
                "token": self._token,
                "compress": False,
                "large_threshold": self._large_threshold,
                "properties": user_agents.UserAgent().websocket_triplet,
                "shard": [self.shard_id, self.shard_count],
            },
        }

        # From october 2020, we will likely just make this always passed
        if self._intents is not None:
            pl["d"]["intents"] = self._intents

        if self._presence:
            # noinspection PyTypeChecker
            pl["d"]["presence"] = self._presence
        await self._send(pl)
        self.logger.debug("sent IDENTIFY")
        self.handshake_event.set()

    async def _resume(self):
        self.logger.debug("preparing to send RESUME")
        pl = {
            "op": codes.GatewayOpcode.RESUME,
            "d": {"token": self._token, "seq": self.seq, "session_id": self.session_id},
        }
        await self._send(pl)
        self.logger.debug("sent RESUME")

    async def _run(self):
        if self.session_id is None:
            await self._identify()
        else:
            await self._resume()

        self.handshake_event.set()

        while not self.requesting_close_event.is_set():
            next_pl = await self._receive()

            op = next_pl["op"]
            d = next_pl["d"]

            if op == codes.GatewayOpcode.DISPATCH:
                self.seq = next_pl["s"]
                event_name = next_pl["t"]

                if event_name == "READY":
                    self.session_id = d["session_id"]
                    version = d["v"]

                    self.logger.debug(
                        "connection is READY (session:%s, version:%s)", self.session_id, version,
                    )

                    self.ready_event.set()

                elif event_name == "RESUMED":
                    self.resumed_event.set()

                    self.logger.debug("connection has RESUMED (session:%s, s:%s)", self.session_id, self.seq)

                self.dispatch(self, event_name, d)

            elif op == codes.GatewayOpcode.HEARTBEAT:
                self.logger.debug("received HEARTBEAT, preparing to send HEARTBEAT ACK to server in response")
                await self._send({"op": codes.GatewayOpcode.HEARTBEAT_ACK})

            elif op == codes.GatewayOpcode.RECONNECT:
                self.logger.debug("instructed by gateway server to restart connection")
                raise errors.GatewayMustReconnectError()

            elif op == codes.GatewayOpcode.INVALID_SESSION:
                can_resume = bool(d)
                self.logger.debug(
                    "instructed by gateway server to %s session", "resume" if can_resume else "restart",
                )
                raise errors.GatewayInvalidSessionError(can_resume)

            elif op == codes.GatewayOpcode.HEARTBEAT_ACK:
                now = time.perf_counter()
                self.heartbeat_latency = now - self.last_heartbeat_sent
                self.logger.debug("received HEARTBEAT ACK (latency:%ss)", self.heartbeat_latency)

            else:
                self.logger.debug("ignoring opcode %s with data %r", op, d)

    async def _receive(self):  # pylint: disable=too-many-branches
        while True:
            message = await self._receive_one_packet()

            if message.type == aiohttp.WSMsgType.TEXT:
                obj = self._json_deserialize(message.data)

                if self._debug:
                    self.logger.debug("receive text payload %r", message.data)
                else:
                    self.logger.debug(
                        "receive text payload (op:%s, t:%s, s:%s, size:%s)",
                        obj.get("op"),
                        obj.get("t"),
                        obj.get("s"),
                        len(message.data),
                    )
                return obj

            if message.type == aiohttp.WSMsgType.BINARY:
                buffer = bytearray(message.data)
                packets = 1
                while not buffer.endswith(b"\x00\x00\xff\xff"):
                    packets += 1
                    message = await self._receive_one_packet()
                    if message.type != aiohttp.WSMsgType.BINARY:
                        raise errors.GatewayError(f"Expected a binary message but got {message.type}")
                    buffer.extend(message.data)

                pl = self._zlib.decompress(buffer)
                obj = self._json_deserialize(pl)

                if self._debug:
                    self.logger.debug("receive %s zlib-encoded packets containing payload %r", packets, pl)

                else:
                    self.logger.debug(
                        "receive zlib payload (op:%s, t:%s, s:%s, size:%s, packets:%s)",
                        obj.get("op"),
                        obj.get("t"),
                        obj.get("s"),
                        len(pl),
                        packets,
                    )
                return obj

            if message.type == aiohttp.WSMsgType.CLOSE:
                close_code = self._ws.close_code
                try:
                    # noinspection PyArgumentList
                    close_code = codes.GatewayCloseCode(close_code)
                except ValueError:
                    pass

                self.logger.debug("connection closed with code %s", close_code)

                if close_code == codes.GatewayCloseCode.AUTHENTICATION_FAILED:
                    raise errors.GatewayInvalidTokenError()

                if close_code in (codes.GatewayCloseCode.SESSION_TIMEOUT, codes.GatewayCloseCode.INVALID_SEQ):
                    raise errors.GatewayInvalidSessionError(False)

                if close_code == codes.GatewayCloseCode.SHARDING_REQUIRED:
                    raise errors.GatewayNeedsShardingError()

                raise errors.GatewayServerClosedConnectionError(close_code)

            if message.type in (aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED):
                if self.requesting_close_event.is_set():
                    self.logger.debug("connection has been marked as closed")
                    raise errors.GatewayClientClosedError()

                self.logger.debug("connection has been marked as closed unexpectedly")
                raise errors.GatewayClientDisconnectedError()

            if message.type == aiohttp.WSMsgType.ERROR:
                ex = self._ws.exception()
                self.logger.debug("connection encountered some error", exc_info=ex)
                raise errors.GatewayError("Unexpected exception occurred") from ex

    async def _receive_one_packet(self):
        packet = await self._ws.receive()
        self.last_message_received = time.perf_counter()
        return packet

    async def _send(self, payload):
        payload_str = self._json_serialize(payload)

        if len(payload_str) > 4096:
            raise errors.GatewayError(
                f"Tried to send a payload greater than 4096 bytes in size (was actually {len(payload_str)}"
            )

        await self._ratelimiter.acquire()
        await self._ws.send_str(payload_str)

        if self._debug:
            self.logger.debug("sent payload %s", payload_str)
        else:
            self.logger.debug("sent payload (op:%s, size:%s)", payload.get("op"), len(payload_str))

    def __str__(self):
        state = "Connected" if self.is_connected else "Disconnected"
        return f"{state} gateway connection to {self._url} at shard {self.shard_id}/{self.shard_count}"

    def __repr__(self):
        this_type = type(self).__name__
        major_attributes = ", ".join(
            (
                f"is_connected={self.is_connected!r}",
                f"heartbeat_latency={self.heartbeat_latency!r}",
                f"presence={self._presence!r}",
                f"shard_id={self.shard_id!r}",
                f"shard_count={self.shard_count!r}",
                f"seq={self.seq!r}",
                f"session_id={self.session_id!r}",
                f"uptime={self.uptime!r}",
                f"url={self._url!r}",
            )
        )

        return f"{this_type}({major_attributes})"

    def __bool__(self):
        return self.is_connected
