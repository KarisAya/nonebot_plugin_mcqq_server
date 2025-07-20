<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# Minecraft Server 消息互通

mcqq 服主版，采用本地读取 log 信息的方法。本插件为 [MCQQ](https://github.com/17TheWord/nonebot-plugin-mcqq) 的二创

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
MCS_LOG_PATH = "D:/MinecraftServer/logs"
# 功能配置
MCS_GROUP_CMD = [] # 群转发触发命令，如果为空则将群聊消息全部转发至服务器。
MCS_GROUP_LIST = ["724024810"] # QQ群
MCS_MC_CMD = ['.bd']
MCS_MC_BROADCAST = '{'all':["724024810"]}' # 一个字典，键是bot_id, 值是本 bot 负责广播的群组列表。
```

_特别注意：当 `MCS_MC_BROADCAST` 的键为 `all` 时 会用第一个 bot 进行广播。并且如果键设置为 `all` 不可以设置其他 bot_

2. 服务端配置文件

在 MC 服务端文件的 `server.properties` 中开启 Rcon

```properties
# rcon
enable-rcon=true
rcon.password=1 # 设置rcon密码，与mcrcon_password一致。
rcon.port=25575 # 设置rcon端口，与mcrcon_port一致。
```

# 使用方法
