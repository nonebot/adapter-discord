<p align="center">
  <a href="https://nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/adapter-discord/master/assets/logo.png" width="200" height="200" alt="nonebot-adapter-discord"></a>
</p>

<div align="center">

# NoneBot-Adapter-Discord

_✨ Discord 协议适配 ✨_

</div>

## 安装

在 NoneBot 项目目录下运行：

```bash
nb adapter install nonebot-adapter-discord
```

需要 Python 3.10+ 和 NoneBot 2.5.0+。想用还没发布的新代码，可以安装 [`master` 分支](https://github.com/nonebot/adapter-discord/tree/master)。

## 使用指南

第一次用的话，按顺序读下面三篇。读完后，你会有一个能在 Discord 里执行的 `/report` 命令。

1. [让机器人连上 Discord](docs/configuration.md)：创建机器人，填好配置，让它上线。
2. [写第一个斜杠命令](docs/application-commands.md)：写一个 `/report`，在 Discord 里执行它。
3. [发送和回复消息](docs/sending-messages.md)：处理耗时操作，发文件和按钮，主动往频道发消息。

已经会写 NoneBot 插件，想查某个方法或事件，看 [API 与事件速查](docs/api-and-events.md)。

出了问题先看[排错](docs/configuration.md#排错)，还解决不了就[提 Issue](https://github.com/nonebot/adapter-discord/issues)。
