# API 与事件速查

写插件时常做两类事：

- **让机器人做事**，比如查一个频道、删一条消息：调用 `bot` 上的方法，适配器会替你请求 Discord 的接口。
- **在某件事发生时做事**，比如有人编辑了消息、有人加入了服务器：写一个事件响应器，处理对应的事件。

这一页告诉你去哪里查这两样东西。还没写过插件的话，先看[写第一个斜杠命令](application-commands.md)。

## 调用 Bot 方法

比如，按频道 ID 和消息 ID 读一条消息的正文：

```python
from nonebot.adapters.discord import Bot


async def read_message_text(bot: Bot, channel_id: int, message_id: int) -> str:
    message = await bot.get_channel_message(
        channel_id=channel_id, message_id=message_id
    )
    return message.content
```

`bot` 从哪来？在处理函数的参数里写上 `bot: Bot`，NoneBot 会把当前机器人传进来，见 [NoneBot 文档：获取事件信息](https://nonebot.dev/docs/tutorial/event-data)。

### 查一个方法该怎么传参

所有方法的签名都在 [`api/client.pyi`](../nonebot/adapters/discord/api/client.pyi) 里，按方法名搜索就能找到。以 `get_channel_message` 为例：

```python
async def get_channel_message(
    self,
    *,
    channel_id: SnowflakeType,
    message_id: SnowflakeType,
) -> MessageGet:
```

- 参数都要写成 `名字=值`，签名里的 `*` 就是这个意思。
- 没有默认值的参数必须传。这里两个都要传。
- `SnowflakeType` 是 Discord 的 ID，直接传整数。
- `->` 后面是返回值。`MessageGet` 有哪些字段，在 [`api/model.py`](../nonebot/adapters/discord/api/model.py) 里查。返回 `None` 的方法（比如 `delete_message`）成功后没有内容可读。
- 方法注释里的 `see` 链接指向 Discord 官方文档，参数含义和需要的权限都在那里。比如 `get_channel_message` 对应 [Get Channel Message](https://docs.discord.com/developers/resources/message#get-channel-message)。

`send_to()` 这类适配器自己加的便捷方法，在 [`bot.py`](../nonebot/adapters/discord/bot.py) 里查。

### 请求失败时

调用失败会抛出异常，这些异常都在 [`exception.py`](../nonebot/adapters/discord/exception.py) 里：

| 情况 | 异常 |
| --- | --- |
| 401 / 403：令牌无效，或者机器人没有权限 | `UnauthorizedException` |
| 429：请求太频繁 | `RateLimitException` |
| 其他 HTTP 错误，比如 404 找不到消息 | `ActionFailed` |
| 网络断开或超时 | `NetworkError` |

`UnauthorizedException` 和 `RateLimitException` 都是 `ActionFailed` 的子类，捕获 `ActionFailed` 能一起接住。

## 处理事件

NoneBot 把事件分成几类，Discord 适配器里是这样分的：

| 事件 | 类别 | 用哪个函数接收 |
| --- | --- | --- |
| 频道和私信里的新消息 | 消息事件 | `on_message()` |
| 编辑消息、成员加入、执行斜杠命令、点击按钮等其他事件 | 通知事件 | `on_notice()` |
| 连接成功、断线重连等 | 元事件 | `on_metaevent()` |

想处理某一种事件，就把处理函数的 `event` 参数写成那个类型，NoneBot 只会把这种事件交给它。比如有人编辑消息时做点事：

```python
from nonebot import on_notice
from nonebot.adapters.discord import MessageUpdateEvent

message_edited = on_notice()


@message_edited.handle()
async def handle_message_edit(event: MessageUpdateEvent) -> None: ...
```

`MessageUpdateEvent` 包括服务器和私信里的编辑。只想要服务器里的，换成 `GuildMessageUpdateEvent`。

事件类都可以从 [`nonebot.adapters.discord`](../nonebot/adapters/discord/__init__.py) 导入，字段和继承关系在 [`event.py`](../nonebot/adapters/discord/event.py) 里查。某个事件什么时候触发，看 Discord 的 [Gateway Events](https://docs.discord.com/developers/events/gateway-events)。

更多响应器的写法，见 [NoneBot 文档：事件响应器](https://nonebot.dev/docs/tutorial/matcher)。

## 常用方法和事件

| 场景 | 相关方法 | 相关事件 |
| --- | --- | --- |
| [消息](https://docs.discord.com/developers/resources/message)：读取、发送、编辑、删除 | `get_channel_message`、`create_message`、`edit_message`、`delete_message` | `MessageCreateEvent`、`MessageUpdateEvent`、`MessageDeleteEvent` |
| [频道](https://docs.discord.com/developers/resources/channel)与[服务器](https://docs.discord.com/developers/resources/guild)：查详情、列出频道 | `get_channel`、`get_guild`、`get_guild_channels` | `ChannelCreateEvent`、`ChannelUpdateEvent`、`GuildUpdateEvent` |
| [成员](https://docs.discord.com/developers/resources/guild#get-guild-member)：查成员、给成员加身份组 | `get_guild_member`、`add_guild_member_role` | `GuildMemberAddEvent`、`GuildMemberUpdateEvent`、`GuildMemberRemoveEvent` |
| [身份组](https://docs.discord.com/developers/resources/guild#get-guild-roles)：列出、创建身份组 | `get_guild_roles`、`create_guild_role` | `GuildRoleCreateEvent`、`GuildRoleUpdateEvent`、`GuildRoleDeleteEvent` |
| [应用命令](https://docs.discord.com/developers/interactions/application-commands)：查全局或服务器命令，命令权限变化 | `get_global_application_commands`、`get_guild_application_commands` | `ApplicationCommandPermissionsUpdateEvent` |
| [交互](https://docs.discord.com/developers/interactions/receiving-and-responding)：首次回应、读取原回应、发后续消息 | `create_interaction_response`、`get_origin_interaction_response`、`create_followup_message` | `ApplicationCommandInteractionEvent`、`ApplicationCommandAutoCompleteInteractionEvent`、`MessageComponentInteractionEvent`、`ModalSubmitInteractionEvent` |
| [表情回应](https://docs.discord.com/developers/resources/message#create-reaction)：添加、移除自己的回应 | `create_reaction`、`delete_own_reaction` | `MessageReactionAddEvent`、`MessageReactionRemoveEvent` |
| [子区](https://docs.discord.com/developers/topics/threads)：从消息创建子区、列出活跃子区 | `start_thread_from_message`、`list_active_guild_threads` | `ThreadCreateEvent`、`ThreadUpdateEvent` |
| [邀请](https://docs.discord.com/developers/resources/channel#create-channel-invite)：查询、创建频道邀请 | `get_channel_invites`、`create_channel_invite` | `InviteCreateEvent`、`InviteDeleteEvent` |
| [投票](https://docs.discord.com/developers/resources/poll)：查某个选项的投票人、结束投票 | `get_answer_voters`、`end_poll` | `MessagePollVoteAddEvent`、`MessagePollVoteRemoveEvent` |
| [服务器活动](https://docs.discord.com/developers/resources/guild-scheduled-event)：列出预定活动 | `list_scheduled_events_for_guild` | `GuildScheduledEventCreateEvent`、`GuildScheduledEventUpdateEvent` |
| [Webhook](https://docs.discord.com/developers/resources/webhook)：列出、创建频道 Webhook | `get_channel_webhooks`、`create_webhook` | `WebhooksUpdateEvent` |
