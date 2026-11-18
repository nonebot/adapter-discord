# 发送和回复消息

这一篇接着改 `/report`：先处理耗时操作，再给回复加上文件和按钮，最后看看怎么主动往频道发消息。

## 处理耗时操作

Discord 规定，用户执行命令后，机器人要在 **3 秒内**回应。超时的话，用户会看到「应用程序未响应」。

查数据库、调用其他接口经常超过 3 秒。这时可以先回一个「正在思考」，等结果出来，再把它改成真正的内容。把 `report.py` 换成：

```python
import asyncio

from nonebot.adapters.discord.commands import on_slash_command

report = on_slash_command(name="report", description="查看报告状态")


@report.handle()
async def show_report_status() -> None:
    await report.send_deferred_response()
    await asyncio.sleep(4)  # 假装查数据库花了 4 秒
    await report.edit_response("报告已生成")
```

重启后执行 `/report`，会先看到机器人「正在思考」，4 秒后变成「报告已生成」。

- `send_deferred_response()` 先告诉 Discord「收到了，正在处理」。它要放在耗时操作前面，最好写在函数第一行。放晚了超过 3 秒，Discord 会报 `404 Unknown Interaction`。
- `edit_response()` 把「正在思考」改成最终内容。

改完之后还想再发一条消息，用 `send_followup_msg()`：

```python
await report.send_followup_msg("处理了 42 条记录")
```

## 发文件、卡片和按钮

一条消息可以由好几段拼成：文字、卡片、文件、按钮等。每一段是一个 `MessageSegment`，用 `+` 连起来。把 `report.py` 换成：

```python
import asyncio

from nonebot.adapters.discord import Message, MessageSegment
from nonebot.adapters.discord.api import Button, ButtonStyle, Embed
from nonebot.adapters.discord.commands import on_slash_command

report = on_slash_command(name="report", description="查看报告状态")


def report_message() -> Message:
    return (
        MessageSegment.text("报告已生成")
        + MessageSegment.embed(Embed(title="日报", description="共处理 42 条记录"))
        + MessageSegment.attachment(file="report.csv", content=b"count\n42\n")
        + MessageSegment.component(
            Button(label="确认收到", style=ButtonStyle.Primary, custom_id="report:ack")
        )
    )


@report.handle()
async def show_report_status() -> None:
    await report.send_deferred_response()
    await asyncio.sleep(4)
    await report.edit_response(report_message())
```

重启后执行 `/report`，会收到一条带卡片、CSV 文件和按钮的报告。

- `Embed` 是带标题和描述的卡片。
- `attachment()` 上传一个文件。`file` 是文件名，`content` 是文件内容。
- `Button` 是按钮。`custom_id` 是你给按钮起的 ID，用户点击时 Discord 会把它传回来，下一节就靠它认出是哪个按钮。

### 响应按钮点击

用户点了按钮，机器人会收到 `MessageComponentInteractionEvent`。它属于通知事件，用 `on_notice()` 来处理。

在 `report.py` 里加上下面的代码，`import` 放到文件开头：

```python
from nonebot import on_notice
from nonebot.adapters.discord import MessageComponentInteractionEvent
from nonebot.adapters.discord.api import ComponentType


async def is_report_button(event: MessageComponentInteractionEvent) -> bool:
    return (
        event.data.component_type == ComponentType.Button
        and event.data.custom_id == "report:ack"
    )


ack = on_notice(rule=is_report_button)


@ack.handle()
async def acknowledge_report() -> None:
    await ack.finish("已确认收到报告")
```

`is_report_button` 是一条规则：只有用户点的是 `custom_id` 为 `report:ack` 的按钮，才会运行下面的处理函数。

重启，重新执行 `/report`，点「确认收到」，机器人会回复「已确认收到报告」。

## 主动往频道发消息

定时推送、通知之类的场景，机器人要自己往某个频道发消息，用 `bot.send_to()`：

```python
await bot.send_to(123456789012345678, report_message())
```

第一个参数是频道 ID，打开开发者模式后右键频道就能复制。处理函数的参数里写上 `bot: Bot`，NoneBot 会把当前机器人传进来，`Bot` 从 `nonebot.adapters.discord` 导入。

## 引用用户的消息

处理普通消息时，加上 `reply_message=True`，机器人的回复会引用用户发的那条消息：

```python
await matcher.finish("收到", reply_message=True)
```

读取普通消息的正文需要额外开权限，见[读取普通消息的正文](configuration.md#读取普通消息的正文)。

想查更多方法和事件，看 [API 与事件速查](api-and-events.md)。
