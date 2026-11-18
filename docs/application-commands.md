# 写第一个斜杠命令

斜杠命令就是在 Discord 输入框里打 `/` 后弹出来的命令。这一篇写一个 `/report`，用户执行后，机器人回复一句话。

开始前，先按[上一篇](configuration.md)让机器人上线。

## 1. 新建插件文件

打开 `pyproject.toml`，找到 `[tool.nonebot]` 下的 `plugin_dirs`，NoneBot 会从这些目录加载插件。比如写的是 `plugin_dirs = ["src/plugins"]`，就新建 `src/plugins/report.py`。

没有 `plugin_dirs` 的话，在 `[tool.nonebot]` 下加一行 `plugin_dirs = ["plugins"]`，再新建 `plugins/report.py`。更多加载方式见 [NoneBot 的插件教程](https://nonebot.dev/docs/tutorial/create-plugin)。

## 2. 写命令

在 `report.py` 中写入：

```python
from nonebot.adapters.discord.commands import on_slash_command

report = on_slash_command(name="report", description="查看报告状态")


@report.handle()
async def show_report_status() -> None:
    await report.finish("报告已生成")
```

- `on_slash_command()` 创建一个斜杠命令。`name` 是用户要输入的命令名，`description` 会显示在命令菜单里。
- `@report.handle()` 下面的函数，就是用户执行 `/report` 时运行的代码。
- `report.finish()` 回复一条消息，然后结束这次处理。

## 3. 在 Discord 里试一下

重新运行 `nb run`。在测试服务器的任意文字频道输入 `/report`，在菜单里选中你的机器人提供的那一项，按回车。机器人会回复「报告已生成」。

菜单里没有这个命令的话，看[排错](configuration.md#排错)。

## 给命令加参数

让用户选择查最近几天的报告。把 `report.py` 换成：

```python
from nonebot.adapters.discord.api import IntegerOption
from nonebot.adapters.discord.commands import CommandOption, on_slash_command

report = on_slash_command(
    name="report",
    description="查看报告状态",
    options=[IntegerOption(name="days", description="查最近几天")],
)


@report.handle()
async def show_report_status(days: CommandOption[int | None]) -> None:
    days = 7 if days is None else days
    await report.finish(f"最近 {days} 天的报告已生成")
```

重启后输入 `/report`，命令后面会多出一个 `days` 选项。填 `3`，机器人回复「最近 3 天的报告已生成」；不填就按 7 天算。

`CommandOption` 会按函数参数的名字取同名选项的值，所以 `IntegerOption(name="days")` 和参数 `days` 要用同一个名字。用户没填时，取到的是 `None`。

想让选项必填，给 `IntegerOption` 加上 `required=True`。

## 更多命令类型

| 想做的事 | 怎么写 |
| --- | --- |
| 一个命令下分几个操作，比如 `/report view` 和 `/report export` | 在 `options` 里用 `SubCommandOption` 定义子命令，每个子命令用 `@report.handle_sub_command("view")` 写处理函数。 |
| 右键一条消息，在「应用」菜单里执行 | 用 `on_message_command()` 创建命令，处理函数里用 `CommandMessage` 拿到被右键的消息。 |
| 右键一个用户，在「应用」菜单里执行 | 用 `on_user_command()` 创建命令，处理函数里用 `CommandUser` 拿到被右键的用户。 |

## 登记新命令

每加一个命令，都要把命令名写进 `.env` 的 `application_commands`，它才会出现在 Discord 里：

```json
"application_commands": {
  "report": ["123456789012345678"],
  "export": ["123456789012345678"]
}
```

命令多了，可以用 `*` 代表全部命令：

```json
"application_commands": {
  "*": ["123456789012345678"]
}
```

服务器 ID 换成 `"*"`，命令就会注册成全局命令，所有加了这个机器人的服务器都能用。

接下来：[发送和回复消息](sending-messages.md)。
