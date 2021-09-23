from enum import Enum
from typing import Callable, Any
import typing

import discord


class DiscordEventType(Enum):
    ON_CONNECT = 0
    ON_SHARD_CONNECT = 1
    ON_DISCONNECT = 2
    ON_SHARD_DISCONNECT = 3
    ON_READY = 4
    ON_SHARD_READY = 5
    ON_RESUMED = 6
    ON_SHARD_RESUMED = 7
    ON_ERROR = 8
    ON_SOCKET_RAW_RECEIVED = 9
    ON_SOCKET_RAW_SEND = 10
    ON_TYPING = 11
    ON_MESSAGE = 12
    ON_MESSAGE_DELETE = 13
    ON_BULK_MESSAGE_DELETE = 14
    ON_RAW_MESSAGE_DELETE = 15
    ON_RAW_BULK_MESSAGE_DELETE = 16
    ON_MESSAGE_EDIT = 17
    ON_RAW_MESSAGE_EDIT = 18
    ON_REACTION_ADD = 19
    ON_RAW_REACTION_ADD = 20
    ON_REACTION_REMOVE = 21
    ON_RAW_REACTION_REMOVE = 22
    ON_REACTION_CLEAR = 23
    ON_RAW_REACTION_CLEAR = 24
    ON_REACTION_CLEAR_EMOJI = 25
    ON_RAW_REACTION_CLEAR_EMOJI = 26
    ON_PRIVATE_CHANNEL_DELETE = 27
    ON_PRIVATE_CHANNEL_CREATE = 28
    ON_PRIVATE_CHANNEL_UPDATE = 29
    ON_PRIVATE_CHANNEL_PINS_UPDATE = 30
    ON_GUILD_CHANNEL_CREATE = 31
    ON_GUILD_CHANNEL_DELETE = 32
    ON_GUILD_CHANNEL_UPDATE = 33
    ON_GUILD_CHANNEL_PINS_UPDATE = 34
    ON_GUILD_INTEGRATIONS_UPDATE = 35
    ON_WEBHOOK_UPDATE = 36
    ON_MEMBER_JOIN = 37
    ON_MEMBER_REMOVE = 38
    ON_MEMBER_UPDATE = 39
    ON_USER_UPDATE = 40
    ON_GUILD_JOIN = 41
    ON_GUILD_REMOVE = 42
    ON_GUILD_UPDATE = 43
    ON_GUILD_ROLE_CREATE = 44
    ON_GUILD_ROLE_DELETE = 45
    ON_GUILD_ROLE_UPDATE = 46
    ON_GUILD_EMOJIS_UPDATE = 47
    ON_GUILD_AVAILABLE = 48
    ON_GUILD_UNAVAILABLE = 49
    ON_VOICE_STATE_UPDATE = 50
    ON_MEMBER_BAN = 51
    ON_MEMBER_UNBAN = 52
    ON_INVITE_CREATE = 53
    ON_INVITE_DELETE = 54
    ON_GROUP_JOIN = 55
    ON_GROUP_REMOVE = 56
    ON_RELATIONSHIP_ADD = 57
    ON_RELATIONSHIP_REMOVE = 58
    ON_RELATIONSHIP_UPDATE = 59


class DiscordEventManager:
    __bot: discord.Client

    __listeners: list[dict[Any, Any]] = []

    def __init__(self, bot: discord.Client) -> None:
        self.__bot = bot
        self.register_listeners()

    def add_listener(self, event_type: DiscordEventType, f: typing.Any) -> None:
        self.__listeners.append({"event_type": event_type, "func": f})

    async def fire_event(self, event_type: DiscordEventType, *args) -> None:
        for listener in self.__listeners:
            if listener["event_type"] == event_type:
                func: typing.Any = listener["func"]
                await func(*args)


    def register_listeners(self) -> None:
        @self.__bot.event
        async def on_connect() -> None:
            await self.fire_event(DiscordEventType.ON_CONNECT)

        @self.__bot.event
        async def on_shard_connect() -> None:
            await self.fire_event(DiscordEventType.ON_SHARD_CONNECT)

        @self.__bot.event
        async def on_disconnect() -> None:
            await self.fire_event(DiscordEventType.ON_DISCONNECT)

        @self.__bot.event
        async def on_shard_disconnect() -> None:
            await self.fire_event(DiscordEventType.ON_SHARD_DISCONNECT)

        @self.__bot.event
        async def on_ready() -> None:
            await self.fire_event(DiscordEventType.ON_READY)

        @self.__bot.event
        async def on_shard_ready() -> None:
            await self.fire_event(DiscordEventType.ON_SHARD_READY)

        @self.__bot.event
        async def on_resumed() -> None:
            await self.fire_event(DiscordEventType.ON_RESUMED)

        @self.__bot.event
        async def on_shard_resumed() -> None:
            await self.fire_event(DiscordEventType.ON_SHARD_RESUMED)



        @self.__bot.event
        async def on_socket_raw_received(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_SOCKET_RAW_RECEIVED, arg0)

        @self.__bot.event
        async def on_socket_raw_send(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_SOCKET_RAW_SEND, arg0)

        @self.__bot.event
        async def on_typing(arg0: Any, arg1: Any, arg2: Any) -> None:
            await self.fire_event(DiscordEventType.ON_TYPING, arg0, arg1, arg2)

        @self.__bot.event
        async def on_message(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MESSAGE, arg0)

        @self.__bot.event
        async def on_message_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MESSAGE_DELETE, arg0)

        @self.__bot.event
        async def on_bulk_message_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_BULK_MESSAGE_DELETE, arg0)

        @self.__bot.event
        async def on_raw_message_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_MESSAGE_DELETE, arg0)

        @self.__bot.event
        async def on_raw_bulk_message_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_BULK_MESSAGE_DELETE, arg0)

        @self.__bot.event
        async def on_message_edit(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MESSAGE_EDIT, arg0, arg1)

        @self.__bot.event
        async def on_raw_message_edit(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_MESSAGE_EDIT, arg0)

        @self.__bot.event
        async def on_reaction_add(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_REACTION_ADD, arg0, arg1)

        @self.__bot.event
        async def on_raw_reaction_add(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_REACTION_ADD, arg0)

        @self.__bot.event
        async def on_reaction_remove(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_REACTION_REMOVE, arg0, arg1)

        @self.__bot.event
        async def on_raw_reaction_remove(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_REACTION_REMOVE, arg0)

        @self.__bot.event
        async def on_reaction_clear(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_REACTION_CLEAR, arg0, arg1)

        @self.__bot.event
        async def on_raw_reaction_clear(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_REACTION_CLEAR, arg0)

        @self.__bot.event
        async def on_reaction_clear_emoji(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_REACTION_CLEAR_EMOJI, arg0)

        @self.__bot.event
        async def on_raw_reaction_clear_emoji(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RAW_REACTION_CLEAR_EMOJI, arg0)

        @self.__bot.event
        async def on_private_channel_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_PRIVATE_CHANNEL_DELETE, arg0)

        @self.__bot.event
        async def on_private_channel_create(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_PRIVATE_CHANNEL_CREATE, arg0)

        @self.__bot.event
        async def on_private_channel_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_PRIVATE_CHANNEL_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_private_channel_pins_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_PRIVATE_CHANNEL_PINS_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_channel_create(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_CHANNEL_CREATE, arg0)

        @self.__bot.event
        async def on_guild_channel_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_CHANNEL_DELETE, arg0)

        @self.__bot.event
        async def on_guild_channel_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_CHANNEL_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_channel_pins_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_CHANNEL_PINS_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_integrations_update(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_INTEGRATIONS_UPDATE, arg0)

        @self.__bot.event
        async def on_webhook_update(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_WEBHOOK_UPDATE, arg0)

        @self.__bot.event
        async def on_member_join(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MEMBER_JOIN, arg0)

        @self.__bot.event
        async def on_member_remove(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MEMBER_REMOVE, arg0)

        @self.__bot.event
        async def on_member_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MEMBER_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_user_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_USER_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_join(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_JOIN, arg0)

        @self.__bot.event
        async def on_guild_remove(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_REMOVE, arg0)

        @self.__bot.event
        async def on_guild_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_role_create(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_ROLE_CREATE, arg0)

        @self.__bot.event
        async def on_guild_role_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_ROLE_DELETE, arg0)

        @self.__bot.event
        async def on_guild_role_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_ROLE_UPDATE, arg0, arg1)

        @self.__bot.event
        async def on_guild_emojis_update(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_EMOJIS_UPDATE, arg0)

        @self.__bot.event
        async def on_guild_available(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_AVAILABLE, arg0)

        @self.__bot.event
        async def on_guild_unavailable(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GUILD_UNAVAILABLE, arg0)

        @self.__bot.event
        async def on_voice_state_update(arg0: Any, arg1: Any, arg2: Any) -> None:
            await self.fire_event(DiscordEventType.ON_VOICE_STATE_UPDATE, arg0, arg1, arg2)

        @self.__bot.event
        async def on_member_ban(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MEMBER_BAN, arg0, arg1)

        @self.__bot.event
        async def on_member_unban(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_MEMBER_UNBAN, arg0, arg1)

        @self.__bot.event
        async def on_invite_create(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_INVITE_CREATE, arg0)

        @self.__bot.event
        async def on_invite_delete(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_INVITE_DELETE, arg0)

        @self.__bot.event
        async def on_group_join(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GROUP_JOIN, arg0, arg1)

        @self.__bot.event
        async def on_group_remove(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_GROUP_REMOVE, arg0, arg1)

        @self.__bot.event
        async def on_relationship_add(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RELATIONSHIP_ADD, arg0)

        @self.__bot.event
        async def on_relationship_remove(arg0: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RELATIONSHIP_REMOVE, arg0)

        @self.__bot.event
        async def on_relationship_update(arg0: Any, arg1: Any) -> None:
            await self.fire_event(DiscordEventType.ON_RELATIONSHIP_UPDATE, arg0, arg1)


