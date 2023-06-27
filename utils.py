from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent
import re

def mc_translate(event: MessageEvent):
    '''
    把信息翻译成 Minecraft 信息命令
    :param bot: Bot
    :param event: Event
    '''
    # 命令信息起始
    if isinstance(event,GroupMessageEvent):
        nikname = lambda event:event.sender.nickname or event.sender.card
        Tip = f"[QQ群]"
    elif isinstance(event,GuildMessageEvent):
        nikname = lambda event:event.sender.nickname or event.sender.card
        Tip = f"[QQ频道]"
    else:
        return ""

    command_msg = 'tellraw @a ["",'
    # 插件名与发言人昵称
    command_msg += '{"text": "' + Tip + nikname(event) + ' 说：","color": "white"},'
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
            command_msg += '{"text": "@' + nikname(event) + ' ","color": "aqua"},'
        # share
        elif msg.type == "share":
            command_msg += '{"text": "[分享：' + msg.data['title'] + '] ","color": "yellow","clickEvent": {"action": "open_url","value": "' + \
               msg.data['url'] + '"},"hoverEvent": {"action": "show_text","contents": [{"text": "查看图片","color": "dark_purple"}]}},'
        else:
            command_msg += '{"text": "[ ' + msg.type + '] ","color": "white"},'
    command_msg += ']'
    command_msg = command_msg.replace("},]", "}]")
    return command_msg

def log_to_dict(loginfo:str) -> dict:
    '''
    转换log信息
    :param loginfo:log信息
    '''
    if res := re.search(": <(.+)>(.+)",loginfo):
        return {"nickname":res.group(1),"message":res.group(2)}
    else:
        return None