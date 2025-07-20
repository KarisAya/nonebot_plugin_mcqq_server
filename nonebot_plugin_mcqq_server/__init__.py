from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_alconna")
require("nonebot_plugin_uninfo")
from . import __main__ as _

# 插件元数据
__plugin_meta__ = PluginMetadata(
    name="Minecraft Server 消息互通",
    description="mcqq服主版，采用本地读取log信息的方法的Minecraft Server消息互通的插件。",
    usage="",
    homepage="https://github.com/KarisAya/nonebot_plugin_mcqq_server",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_uninfo",
    ),
)
