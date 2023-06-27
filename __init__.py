from pathlib import Path
from nonebot import get_driver, on_message, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    MessageEvent,
    GroupMessageEvent,
    GROUP_ADMIN,
    GROUP_OWNER
    )
from nonebot.permission import SUPERUSER
from nonebot_plugin_guild_patch import GuildMessageEvent
from nonebot.log import logger
from mcrcon import MCRcon
import time
import asyncio

from .config import (
    group_list,
    guild_list,
    mc_log_path,
    mcrcon_password,
    mcrcon_port
    )
from .utils import mc_translate, log_to_dict

driver = get_driver()

switch = False

async def set_switch_rule(bot:Bot,event:MessageEvent, permission = SUPERUSER | GROUP_ADMIN | GROUP_OWNER,):
    if event.to_me and await permission(bot,event):
        cmd = str(event.message)
        global switch
        if cmd in {"打开互通","开启互通"}:
            if switch:
                await bot.send(event,"开启失败，因为你正在与Minecraft服务器的连接中")
                return False
            else:
                await bot.send(event,"已开启与Minecraft服务器的连接")
                return True
        elif cmd in {"关闭互通","停止互通"}:
            switch = False
            await bot.send(event,"已关闭与Minecraft服务器的连接")
    return False

async def MC_TO_QQ(bot: Bot):
    global switch
    if switch:
        logger.error("MC_TO_QQ未开启")
        return
    logger.success("MC_TO_QQ已开启")
    switch = True
    with open(log, "r", encoding = "utf8") as fp:
        pos = fp.seek(0,2)
    while switch:
        fp = open(log, "r", encoding = "utf8")
        fp.seek(pos, 0)
        if line := fp.read():
            pos = fp.seek(0,2)
            line.replace("\r\n","\n")
            line = line.strip('\n').split('\n')
            for x in line:
                if msg_dict := log_to_dict(x):
                    msg = f'【{msg_dict["nickname"]}】{msg_dict["message"]}'
                    for group in group_list:
                        await bot.send_group_msg(group_id = group,message = msg)
                    for guild in guild_list:
                        await bot.send_guild_channel_msg(guild_id = guild['guild_id'],channel_id = guild['channel_id'],message = msg)
        fp.close()
        await asyncio.sleep(1)
    logger.success("MC_TO_QQ已关闭")


receive = on_message(rule = set_switch_rule, priority = 10, block = True)

log = Path(mc_log_path) / "latest.log"
if log.exists():
    logger.success(f"已找到 {log}")
    receive.append_handler(MC_TO_QQ)
    driver.on_bot_connect(MC_TO_QQ)
else:
    logger.error(f"mc_log_path 地址设置错误，{log} 不存在。")

mcr = MCRcon("127.0.0.1", mcrcon_password, mcrcon_port)

async def QQ_TO_MC(event: Event):
    global mcrcon_connect_is_running
    if mcrcon_connect_is_running:
        return
    global mcr
    timeout = time.time() + 30
    while time.time() < timeout:
        try:
            mcr.command(mc_translate(event))
            break
        except (OSError, ConnectionRefusedError) as e:
            logger.error(f"信息发送失败：{e}")
            await mcrcon_connect(mcr)

mcrcon_connect_is_running = False

async def mcrcon_connect(mcr:MCRcon):
    global mcrcon_connect_is_running
    mcrcon_connect_is_running = True
    try:
        mcr.connect()
        mcrcon_connect_is_running = False
        logger.success("与 MCRcon 连接成功！")
    except (OSError, ConnectionRefusedError) as e:
        logger.info(f"与 MCRcon 连接失败，正在重新连接...{e}")
        await asyncio.sleep(3)
        await mcrcon_connect(mcr)

async def CUSTOMER(event: MessageEvent) -> bool:
    if isinstance(event,GroupMessageEvent):
        return event.group_id in group_list
    if isinstance(event,GuildMessageEvent):
        for guild in guild_list:
            if event.guild_id == guild["guild_id"] and event.channel_id == guild["channel_id"]:
                return True
        else:
            return False
    return False

send = on_message(rule = lambda :switch and not mcrcon_connect_is_running, permission = CUSTOMER, priority = 10)
send.append_handler(QQ_TO_MC)