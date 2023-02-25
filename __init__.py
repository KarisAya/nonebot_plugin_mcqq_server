from nonebot import get_driver, on_message, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN,GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.log import logger

import nonebot
import asyncio
import mcrcon

from nonebot_plugin_guild_patch import GuildMessageEvent
from pathlib import Path
from .utils import (
    group_list,
    guild_list,
    mc_log_path,
    mcrcon_password,
    mcrcon_port
    )
from .utils import mcrcon_connect, mc_translate, log_to_dict

switch = True

switch_ON = on_command(
    "打开互通",
    aliases = {"开启互通"},
    rule = to_me(),
    permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority = 10,
    block = True
    )

@switch_ON.handle()
async def _():
    global switch
    switch = True
    await switch_ON.finish("已开启与Minecraft服务器的连接")

switch_OFF = on_command(
    "关闭互通",
    aliases = {"停止互通"},
    rule = to_me(),
    permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority = 10,
    block = True
    )

@switch_OFF.handle()
async def _():
    global switch
    switch = False
    await switch_OFF.finish("已临时屏蔽与Minecraft服务器的连接")

log = Path(mc_log_path) / "latest.log"
if log.exists():
    logger.success(f"已找到 {log}")
    driver = get_driver()
    @driver.on_bot_connect
    async def _(bot: Bot):
        global switch
        with open(log, "r", encoding = "utf8") as fp:
            pos = fp.seek(0,2)
        while True:
            fp = open(log, "r", encoding = "utf8")
            fp.seek(pos, 0)
            line = fp.read()
            if line:
                pos = fp.seek(0,2)
                if switch:
                    line.replace("\r\n","\n")
                    line = line.strip('\n').split('\n')
                    for x in line:
                        msg_dict = log_to_dict(x)
                        if msg_dict:
                            msg = f'【{msg_dict["nickname"]}】{msg_dict["message"]}'
                            for group in group_list:
                                await bot.send_group_msg(group_id = group,message = msg)
                            for guild in guild_list:
                                await bot.send_guild_channel_msg(guild_id = guild['guild_id'],channel_id = guild['channel_id'],message = msg)
            fp.close()
            await asyncio.sleep(1)
else:
    logger.error(f"mc_log_path 地址设置错误，{log} 不存在。")

# 定义CUSTOMER权限

async def CUSTOMER(event: MessageEvent) -> bool:
    if isinstance(event,GroupMessageEvent):
        return event.group_id in group_list
    elif isinstance(event,GuildMessageEvent):
        for guild in guild_list:
            if event.guild_id == guild["guild_id"] and event.channel_id == guild["channel_id"]:
                return True
        else:
            return False
    else:
        return False

mcr = asyncio.run(mcrcon_connect("127.0.0.1", mcrcon_password, mcrcon_port))
flag = True

async def check():
    return switch and (mcr or flag)

send = on_message(rule = check, permission = CUSTOMER, priority = 10)

@send.handle()
async def _(bot: Bot, event: Event):
    global flag, mcr
    msg = await mc_translate(bot, event)
    try:
        mcr.command(msg)
        flag = True
    except (mcrcon.MCRconException, ConnectionResetError, ConnectionAbortedError):
        flag = False
        mcr = await mcrcon_connect("127.0.0.1", mcrcon_password, mcrcon_port)
        mcr.command(msg)
    except AttributeError:
        flag = False
        mcr = await mcrcon_connect("127.0.0.1", mcrcon_password, mcrcon_port)
    except Exception as e:
        flag = True
        logger.error(f"与 MCRcon 的连接出现错误：{e}")