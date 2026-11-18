# 让机器人连上 Discord

做完这一篇，你的机器人会在 Discord 上显示为在线。

开始前需要一个 NoneBot 项目。还没有的话，先跟着 [NoneBot 快速上手](https://nonebot.dev/docs/quick-start)用 `nb create` 建一个。

## 1. 在 Discord 创建机器人

1. 打开 [Discord Developer Portal](https://discord.com/developers/applications)，点 **New Application** 新建一个应用。
2. 进入 **Bot** 页面，点 **Reset Token**，复制令牌（Token），后面要用。令牌相当于机器人的密码，别人拿到就能操控你的机器人，不要外传。
3. 进入 **Installation** 页面：
   - **Installation Contexts** 勾选 **Guild Install**。
   - **Default Install Settings** 的 Guild Install 里，Scopes 选 `bot` 和 `applications.commands`，Permissions 选 **View Channels** 和 **Send Messages**。
4. 复制同一页的 **Install Link**，用浏览器打开，把机器人加到你的测试服务器。

具体界面可以对照 [Discord 官方的安装步骤](https://docs.discord.com/developers/quick-start/getting-started#setting-up-an-install-link)。

> [!TIP]
> 建议专门建一个应用来练习。机器人启动时，会用代码里的命令覆盖它在服务器上原有的命令。

## 2. 安装适配器和驱动器

适配器需要两个驱动器：HTTPX 用来调用 Discord 的接口，websockets 用来和 Discord 保持连接。在项目目录运行：

```bash
nb adapter install nonebot-adapter-discord
nb driver install httpx
nb driver install websockets
```

## 3. 填写配置

先拿到测试服务器的 ID：在 Discord 里打开**用户设置 → 高级 → 开发者模式**，然后右键服务器图标，点**复制服务器 ID**。

打开项目根目录的 `.env`，写入下面的内容，把令牌和服务器 ID 换成你自己的：

```dotenv
DRIVER=~httpx+~websockets
DISCORD_BOTS='
[
  {
    "token": "替换为 Bot Token",
    "application_commands": {
      "report": ["123456789012345678"]
    }
  }
]
'
```

这几项的意思：

- `DRIVER`：让 NoneBot 使用刚装的两个驱动器。如果项目里还有别的适配器在用 FastAPI 等驱动器，就连起来写，比如 `~fastapi+~httpx+~websockets`。
- `DISCORD_BOTS`：机器人列表，一个机器人对应一组 `{}`。整段内容要用单引号包起来。
- `application_commands`：把哪些斜杠命令注册到哪些服务器。这里写的是把 `/report` 注册到你的测试服务器，[下一篇](application-commands.md)就来写这个命令。

`.env.dev`、`.env.prod` 里的配置会覆盖 `.env`。如果那里也写了 `DRIVER`，记得一起改。

在国内连不上 Discord 的话，再加一行代理，地址换成你自己的：

```dotenv
DISCORD_PROXY=http://127.0.0.1:7890
```

## 4. 启动

在项目目录运行：

```bash
nb run
```

日志里出现 `Bot <机器人 ID> connected`，Discord 成员列表里机器人显示为在线，就成功了。

接下来：[写第一个斜杠命令](application-commands.md)。

## 排错

| 现象 | 处理方法 |
| --- | --- |
| 启动后一直连不上，日志里是网络错误或超时 | 确认这台机器能访问 Discord。国内网络一般要配置 `DISCORD_PROXY`。 |
| 启动时报令牌或认证错误 | 令牌填错了，或者在网页上重置过。回到 **Bot** 页面重新复制。 |
| 启动时报驱动器加载失败 | 驱动器要装在运行机器人的那个 Python 环境里。在项目目录重新执行上面的安装命令。 |
| 输入 `/` 后菜单里没有 `/report` | 看启动日志，确认插件已经加载，同步命令时没有报错；再检查 `.env` 里的服务器 ID。 |
| 能看到 `/report`，执行后提示「应用程序未响应」 | 打开 Developer Portal 的 **General Information** 页面，清空 **Interactions Endpoint URL** 并保存。这一项填了地址，Discord 会把命令发到那个地址，机器人就收不到了。 |

### 读取普通消息的正文

默认情况下，机器人能收到频道里的新消息，但读到的正文是空的，只有 @机器人的消息和私信例外。这是 Discord 的隐私限制，读正文需要单独打开 Message Content 权限。

只用斜杠命令的话，可以跳过这一步。需要读正文时：

1. 在 Developer Portal 的 **Bot → Privileged Gateway Intents** 打开 **Message Content Intent**。
2. 在 `.env` 里给这个机器人加上 `intent` 一项：

   ```dotenv
   DISCORD_BOTS='
   [
     {
       "token": "替换为 Bot Token",
       "intent": {"message_content": true},
       "application_commands": {
         "report": ["123456789012345678"]
       }
     }
   ]
   '
   ```

3. 重启机器人。

全部配置项和默认值写在 [`config.py`](../nonebot/adapters/discord/config.py) 里。
