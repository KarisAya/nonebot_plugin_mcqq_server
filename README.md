<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>
<div align="center">

# nonebot_plugin_mcqq_server

mcqq服主版，采用本地读取log信息的方法。

本插件为 [mcqq](https://github.com/KarisAya/nonebot-plugin-mcqq) 的二创

</div>

## 需要安装

[nonebot_plugin_guild_patch](https://github.com/mnixry/nonebot-plugin-guild-patch) NoneBot2 QQ 频道 (go-cqhttp) 支持适配补丁插件

## 安装

    pip install nonebot_plugin_mcqq_server

## 使用

    nonebot.load_plugin('nonebot_plugin_mcqq_server')
    
## 配置
    # nonebot_plugin_mcqq_server
    guild_list = [{"guild_id": 47724881662376582, "channel_id": 10880356}] # QQ频道
    mc_log_path = "D:/MinecraftServer/logs" # log文件夹地址
    mc_ip: str = "127.0.0.1"    # 服务器 IP
    mcrcon_password: str = "1"  # MCRcon password
    mcrcon_port: int = 25575    # MCRcon 端口

### `guild_list` 配置QQ频道

格式：

    guild_list: list = [
        {"guild_id": 0, "channel_id": 0},
        {"guild_id": 1, "channel_id": 1}
        ]
        
列表元素为字典，字典中的 "guild_id"：频道ID，"channel_id":子频道ID

获取频道ID和子频道ID的方法：

把bot拉进频道里，在频道里发一条消息，运行gocq的终端上会出现类似这样的INFO

    [2022-09-09 01:36:29] [INFO]: 收到来自频道 樱桃味文酱的游戏频道(47724881662376582) 子频道 闲聊(10880356) 内 小叶叶叶子(144115218933268761) 的消息: hello

频道ID：47724881662376582

子频道ID：10880356

## Todo:

- [x] QQ频道适配
- [ ] 群聊适配
- [ ] 远程服务器模式
