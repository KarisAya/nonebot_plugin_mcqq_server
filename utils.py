from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Event, Message
from nonebot.log import logger
from mcrcon import MCRcon

import nonebot
import time
import asyncio

from nonebot_plugin_guild_patch import GuildMessageEvent

from .config import Config

global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config.dict())

group_list = config.group_list
guild_list = config.guild_list
mc_log_path = config.mc_log_path
mc_ip = config.mc_ip
mcrcon_password = config.mcrcon_password
mcrcon_port = config.mcrcon_port

async def mcrcon_connect(mc_ip: str,mcrcon_password: str, mcrcon_port:int):
    """
    与 mcrcon 建立连接
    :param mc_ip: 服务器 IP
    :param mcrcon_password: MCRcon password
    :param mcrcon_port: MCRcon 端口
    """
    mcr = MCRcon(mc_ip,mcrcon_password,mcrcon_port)
    try:
        mcr.connect()
        logger.success("与 MCRcon 连接成功！")
        return mcr
    except (OSError, ConnectionRefusedError):
        nonebot.logger.info("与 MCRcon 连接失败，正在重新连接...")
        await asyncio.sleep(0.5)
        await mcrcon_connect(mc_ip, mcrcon_password, mcrcon_port)

async def mc_translate(bot: Bot, event: Event):
    '''
    把信息翻译成 Minecraft 信息命令
    :param bot: Bot
    :param event: Event
    '''
    # 命令信息起始
    if isinstance(event,GroupMessageEvent):
        nikname = group_nickname
        Tip = f"[QQ群]"
    elif isinstance(event,GuildMessageEvent):
        nikname = guild_nickname
        Tip = f"[QQ频道]"
    else:
        return ""

    command_msg = 'tellraw @a ["",'
    # 插件名与发言人昵称
    command_msg += '{"text": "' + Tip + (event.sender.card or event.sender.nickname) + ' 说：","color": "white"},'
    # 文本信息
    text_msg = ''
    for msg in event.message:
        # 文本
        if msg.type == "text":
            command_msg += '{"text": "' + msg.data['text'].replace("\r\n", " ") + ' ","color": "white"},'
        # 图片
        elif msg.type == "image":
            command_msg += '{"text": "[图片] ","color": "yellow","clickEvent": {"action": "open_url","value": "' + \
                msg.data['url'] + '"},"hoverEvent": {"action": "show_text","contents": [{"text": "查看图片","color": "dark_purple"}]}},'
        # 表情
        elif msg.type == "face":
            command_msg += '{"text": "[表情] ","color": "white"},'
        # 语音
        elif msg.type == "record":
            command_msg += '{"text": "[语音] ","color": "white"},'
        # 视频
        elif msg.type == "video":
            command_msg += '{"text": "[视频] ","color": "yellow","clickEvent": {"action": "open_url","value": "' + \
                msg.data['url'] + '"},"hoverEvent": {"action": "show_text","contents": [{"text": "查看视频","color": "dark_purple"}]}},'
        # @
        elif msg.type == "at":
            command_msg += '{"text": "@' + await nikname(bot, event, str(msg.data["qq"])) + ' ","color": "aqua"},'
        # share
        elif msg.type == "share":
            command_msg += '{"text": "[分享：' + msg.data['title'] + '] ","color": "yellow","clickEvent": {"action": "open_url","value": "' + \
               msg.data['url'] + '"},"hoverEvent": {"action": "show_text","contents": [{"text": "查看图片","color": "dark_purple"}]}},'
        else:
            command_msg += '{"text": "[ ' + msg.type + '] ","color": "white"},'
    command_msg += ']'
    command_msg = command_msg.replace("},]", "}]")
    return command_msg

async def group_nickname(bot: Bot, event: GroupMessageEvent, user_id: str) -> str:
    data = await bot.get_group_member_info(group_id = event.group_id, user_id = user_id)
    return data["card"] or data["nickname"]

async def guild_nickname(bot: Bot, event: GuildMessageEvent, user_id: str) -> str:
    data = await bot.get_guild_member_profile(guild_id = event.guild_id, user_id = user_id)
    return data['nickname']


def log_to_dict(loginfo:str) -> dict:
    '''
    转换log信息
    :param loginfo:log信息
    '''
    l = loginfo.find('<')
    r = loginfo.find('>')
    if l != -1 and r != -1:
        return {
            "type":"message",
            "nickname":loginfo[l+1:r],
            "message":loginfo[r+2:]
            }
    else:
        x = loginfo.find(':')
        return {
            "type":"log",
            "log":loginfo[:x],
            "info":loginfo[x+2:]
            }