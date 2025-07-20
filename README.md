<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# Minecraft Server 消息互通

Minecraft Server 消息互通，采用本地读取 log 信息的方法。

[![python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![license](https://img.shields.io/github/license/KarisAya/nonebot_plugin_mcqq_server.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot_plugin_mcqq_server.svg)](https://pypi.python.org/pypi/nonebot_plugin_mcqq_server)
[![pypi download](https://img.shields.io/pypi/dm/nonebot_plugin_mcqq_server)](https://pypi.python.org/pypi/nonebot_plugin_mcqq_server)
<br />

[![机器人 bug 研究中心](https://img.shields.io/badge/QQ%E7%BE%A4-744751179-maroon?)](https://qm.qq.com/q/3vpD9Ypb0c)

</div>

# 安装

```bash
nb plugin install nonebot-plugin-mcqq-server
```

# Bot 配置与服务端配置

1. Bot 配置文件

在 nb 项目路径下找到 `.env.prod` 文件，添加以下内容

```dotenv
# Minecraft Server 消息互通
MCRCON_PASSWORD = "A"
MCRCON_PORT = 25575
MCS_LOG_PATH = "D:/MinecraftServer/logs/latest.log"
# 功能配置
MCS_GROUP_CMD = []
MCS_GROUP_LIST = ["724024810"] # QQ群
MCS_MC_CMD = []
MCS_MC_BROADCAST = '{"all":["724024810"]}'。
```

配置说明：

- `MCRCON_PASSWORD` rcon 密码
- `MCRCON_PORT` rcon 端口
- `MCS_LOG_PATH` 服务端日志文件路径，精确到日志文件
- `MCS_GROUP_CMD` 群转发触发命令，如果为空则将群聊消息全部转发至服务器。
- `MCS_GROUP_LIST` 转发至服务器的群组列表
- `MCS_MC_CMD` 服务器广播命令，如果为空则将服务器消息全部转发至群组。
- `MCS_MC_BROADCAST` 广播分配配置，键是 Bot ID, 值是该 Bot 负责广播的群组列表

_特别注意：当 `MCS_MC_BROADCAST` 的键为 `all` 时为单 bot 模式会，此时插件会用第一个 bot 进行广播。如果键设置为 `all` 不可以设置其他 bot_

2. 服务端配置文件

在 MC 服务端文件的 `server.properties` 中开启 Rcon

```properties
# rcon
enable-rcon=true
rcon.password=1 # 设置rcon密码，与mcrcon_password一致。
rcon.port=25575 # 设置rcon端口，与mcrcon_port一致。
```

# 使用方法

在群内或游戏中发送信息即可使用。

超级管理员可使用 `mcs指令` 向服务器发送控制台指令。

例如 `mcs指令 weather rain` 相当于输入控制台指令 `/weather rain`

# 致谢

- [MCQQ](https://github.com/17TheWord/nonebot-plugin-mcqq)
