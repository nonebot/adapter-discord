<p align="center">
  <a href="https://nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/adapter-discord/master/assets/logo.png" width="200" height="200" alt="nonebot-adapter-discord"></a>
</p>

<div align="center">

# NoneBot-Adapter-Discord

_✨ Discord 协议适配 ✨_

</div>

## 安装

通过 `nb adapter install nonebot-adapter-discord` 安装本适配器。

或在 `nb create` 创建项目时选择 `Discord` 适配器。

可通过 `pip install git+https://github.com/nonebot/adapter-discord.git@master` 安装开发中版本。

由于 [Discord 文档](https://discord.com/developers/docs/intro)存在部分表述不清的地方，并且结构复杂，存在很多 `partial object`，
需要更多实际测试以找出问题，欢迎提出 ISSUE 反馈。

## 配置

修改 NoneBot 配置文件 `.env` 或者 `.env.*`。

### Driver

参考 [driver](https://nonebot.dev/docs/tutorial/configuration#driver) 配置项，添加 `ForwardDriver` 支持。

如：

```dotenv
DRIVER=~httpx+~websockets
```

### DISCORD_BOTS

配置机器人帐号，如：

```dotenv
DISCORD_BOTS='
[
  {
    "token": "xxx",
    "intent": {
      "guild_messages": true,
      "direct_messages": true,
      "message_content": true
    },
    "application_commands": {"*": ["*"]}
  }
]
'

# application_commands的{"*": ["*"]}代表将全部应用命令注册为全局应用命令
# {"admin": ["123", "456"]}则代表将admin命令注册为id是123、456服务器的局部命令，其余命令不注册
```

> **⚠️ 关于 `message_content` Intent**
>
> `message_content` 是 Discord 的**特权 Intent（Privileged Intent）**，默认关闭。
> 若未开启，Bot **仅在以下场景能收到消息内容**，其余情况 `event.content` 为空：
> - 消息中 @ 了 Bot
> - 消息回复了 Bot
> - 私信（DM）消息
>
> 如需正常接收所有频道消息内容，需要：
> 1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) → 你的应用 → **Bot** 页面，开启 **Message Content Intent**
> 2. 在配置中将 `message_content` 设为 `true`

### DISCORD_COMPRESS

是否启用数据压缩，默认为 `False`，如：

```dotenv
DISCORD_COMPRESS=True
```

### DISCORD_API_VERSION

Discord API 版本，默认为 `10`，如：

```dotenv
DISCORD_API_VERSION=10
```

### DISCORD_API_TIMEOUT

Discord API 超时时间，默认为 `30` 秒，如：

```dotenv
DISCORD_API_TIMEOUT=15.0
```

### DISCORD_HANDLE_SELF_MESSAGE

是否处理自己发送的消息，默认为 `False`，如：

```dotenv
DISCORD_HANDLE_SELF_MESSAGE=True
```

### DISCORD_PROXY

代理设置，默认无，如：

```dotenv
DISCORD_PROXY='http://127.0.0.1:6666'
```

## 常见用法

常见插件只需要使用 `Bot.send`、`Message` 和 `MessageSegment`。`Bot.send` 接受字符串、`Message` 或 `MessageSegment`，并负责将消息编译为 Discord 请求；不需要先调用 `parse_message` 或手工拼装 payload。

```python
from nonebot import on_command
from nonebot.params import CommandArg

from nonebot.adapters.discord import Bot, Message, MessageEvent, MessageSegment

matcher = on_command("send")


@matcher.handle()
async def ready(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    text = msg.extract_plain_text()
    message = Message()

    if text == "mention_me":
        message += MessageSegment.text("你好，")
        message += MessageSegment.mention_user(event.user_id)
    elif text == "attachment":
        with open("logo.png", "rb") as file:
            message += MessageSegment.attachment(
                file="logo.png",
                content=file.read(),
            )
    else:
        message += MessageSegment.text(text)

    await bot.send(event, message)
```

以下是一个 Discord 斜杠命令的插件示例。首次响应有三秒时限；耗时任务应通过依赖注入取得 `CommandResponse`，先 `defer()`，完成后再 `respond()`。`CommandResponse` 只能在适配器正在处理 interaction 的上下文中注入，不能在普通事件或脱离处理上下文的代码中取得。

```python
import asyncio
from typing import Optional

from nonebot.adapters.discord import CommandResponse
from nonebot.adapters.discord.api import (
    IntegerOption,
    NumberOption,
    StringOption,
    SubCommandOption,
    User,
    UserOption,
)
from nonebot.adapters.discord.commands import (
    CommandOption,
    on_slash_command,
)

matcher = on_slash_command(
    name="permission",
    description="权限管理",
    options=[
        SubCommandOption(
            name="add",
            description="添加",
            options=[
                StringOption(
                    name="plugin",
                    description="插件名",
                    required=True,
                ),
                IntegerOption(
                    name="priority",
                    description="优先级",
                    required=False,
                ),
            ],
        ),
        SubCommandOption(
            name="remove",
            description="移除",
            options=[
                StringOption(name="plugin", description="插件名", required=True),
                NumberOption(name="time", description="时长", required=False),
            ],
        ),
        SubCommandOption(
            name="ban",
            description="禁用",
            options=[
                UserOption(name="user", description="用户", required=False),
            ],
        ),
    ],
)


@matcher.handle_sub_command("add")
async def handle_user_add(
    plugin: CommandOption[str],
    priority: CommandOption[Optional[int]],
    response: CommandResponse,
):
    # defer() 占用首次响应；ephemeral=True 使原始响应仅对调用者可见。
    await response.defer(ephemeral=True)
    await asyncio.sleep(2)
    await response.respond(f"你添加了插件 {plugin}，优先级 {priority}")
    await asyncio.sleep(2)
    followup = await response.followup(
        f"你添加了插件 {plugin}，优先级 {priority} (新消息)"
    )
    await asyncio.sleep(2)
    await matcher.edit_followup_msg(
        followup.id,
        f"你添加了插件 {plugin}，优先级 {priority} (新消息修改后)",
    )


@matcher.handle_sub_command("remove")
async def handle_user_remove(
    plugin: CommandOption[str],
    time: CommandOption[Optional[float]],
):
    await matcher.send(f"你移除了插件 {plugin}，时长 {time}")


@matcher.handle_sub_command("ban")
async def handle_admin_ban(user: CommandOption[User]):
    await matcher.finish(f"你禁用了用户 {user.username}")
```

## 1.x 迁移与弃用

新代码应传递 `Message`/`MessageSegment` 给 `Bot.send` 或 `Bot.send_to`，并为斜杠命令注入 `CommandResponse`。以下 1.x 兼容接口仍然保留，但 removal target 是 **2.0**：

- `nonebot.adapters.discord.message.parse_message`；
- `ApplicationCommandMatcher.send_deferred_response`；
- `ApplicationCommandMatcher.send_response`；
- `ApplicationCommandMatcher.send_followup_msg`。

此外，在没有 managed interaction context 时，`Bot.send(interaction, ...)` 遇到 `ActionFailed` 后自动创建 followup 的 legacy fallback 也会在 **2.0** 删除。请改为在 interaction handler 中注入 `CommandResponse`，显式调用 `defer()`、`respond()` 或 `followup()`，以便由状态机管理首次响应。

## 高级 raw API

`nonebot.adapters.discord.api` 是长期保留的高级 raw API，**不弃用，也不会随上述 2.0 迁移删除**。需要直接构造 Discord request/response model 或调用原始 endpoint 时，可以继续使用：

```python
from nonebot.adapters.discord.api import *
```

例如 raw 用户仍可直接调用 `bot.create_interaction_response`，以及 original response 的 `get_origin_interaction_response`、`edit_origin_interaction_response`、`delete_origin_interaction_response` 和 followup 的 `create/get/edit/delete_followup_message` CRUD。高层 `CommandResponse` 只是 interaction handler 内更安全的常见路径，不会取代或隐藏这些 raw endpoint。
