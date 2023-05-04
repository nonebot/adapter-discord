<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot-adapter-discord"></a>
</p>

<div align="center">

# NoneBot-Adapter-Discord

_✨ Discord 协议适配 ✨_

</div>

## 说明

本适配器仍在开发中。

目前请通过`pip install git+https://github.com/CMHopeSunshine/adapter-discord.git@dev` 安装。

由于Discord文档存在部分表述不清的地方，并且结构复杂，有很多`partial object`，
给开发带来了很大的困难，因此欢迎大家帮忙测试，提出issue，感谢。

## 配置

修改 NoneBot 配置文件 `.env` 或者 `.env.*`。

### Driver

参考 [driver](https://v2.nonebot.dev/docs/tutorial/configuration#driver) 配置项，添加 `ForwardDriver` 支持。

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
      "direct_messages": true
    }
  }
]
'
```

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

## 使用

### 注册适配器

参考[adapter](https://v2.nonebot.dev/docs/advanced/adapter)注册本适配器，例如：

```python
import nonebot
from nonebot.adapters.discord import Adapter as DiscordAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(DiscordAdapter)

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
```

### 编写插件

以下是一个简单的插件示例，展示各种消息段：

```python
import datetime

from nonebot import on_command
from nonebot.params import CommandArg

from nonebot.adapters.discord import Bot, MessageEvent, MessageSegment, Message
from nonebot.adapters.discord.api import *

matcher = on_command('send')


@matcher.handle()
async def ready(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    # 调用discord的api
    self_info = await bot.get_current_user()  # 获取机器人自身信息
    user = await bot.get_user(user_id=event.user_id)  # 获取指定用户信息
    ...
    # 各种消息段
    msg = msg.extract_plain_text()
    if msg == 'mention_me':
        # 发送一个提及你的消息
        await matcher.finish(MessageSegment.mention_user(event.user_id))
    elif msg == 'time':
        # 发送一个时间，使用相对时间（RelativeTime）样式
        await matcher.finish(MessageSegment.timestamp(datetime.datetime.now(),
                                                      style=TimeStampStyle.RelativeTime))
    elif msg == 'mention_everyone':
        # 发送一个提及全体成员的消息
        await matcher.finish(MessageSegment.mention_everyone())
    elif msg == 'mention_channel':
        # 发送一个提及当前频道的消息
        await matcher.finish(MessageSegment.mention_channel(event.channel_id))
    elif msg == 'embed':
        # 发送一个嵌套消息，其中包含a embed标题，nonebot logo描述和来自网络url的logo图片
        await matcher.finish(MessageSegment.embed(
            Embed(title='a embed',
                  type=EmbedTypes.image,
                  description='nonebot logo',
                  image=EmbedImage(
                      url='https://v2.nonebot.dev/logo.png'))))
    elif msg == 'attachment':
        # 发送一个附件，其中包含来自本地的logo.png图片
        with open('logo.png', 'rb') as f:
            await matcher.finish(MessageSegment.attachment(file='logo.png',
                                                           content=f.read()))
    elif msg == 'component':
        # 发送一个复杂消息，其中包含一个当前时间，一个字符串选择菜单，一个用户选择菜单和一个按钮
        time_now = MessageSegment.timestamp(datetime.datetime.now())
        string_select = MessageSegment.component(
            SelectMenu(type=ComponentType.StringSelect,
                       custom_id='string select',
                       placeholder='select a value',
                       options=[
                           SelectOption(label='A', value='a'),
                           SelectOption(label='B', value='b'),
                           SelectOption(label='C', value='c')]))
        select = MessageSegment.component(SelectMenu(
            type=ComponentType.UserInput,
            custom_id='user_input',
            placeholder='please select a user'))
        button = MessageSegment.component(
            Button(label='button',
                   custom_id='button',
                   style=ButtonStyle.Primary))
        await matcher.finish('now time:' + time_now + string_select + select + button)
    else:
        # 发送一个文本消息
        await matcher.finish(MessageSegment.text(msg))
```
