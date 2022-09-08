from nonebot import get_driver, on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,Message
from nonebot.log import logger

import nonebot
import asyncio
import mcrcon

from nonebot_plugin_guild_patch import GuildMessageEvent
from pathlib import Path
from .utils import (
   guild_list,
   mc_log_path,
   mc_ip,
   mcrcon_password,
   mcrcon_port
   )
from .utils import mcrcon_connect, mc_translate, log_to_dict

log = Path(mc_log_path) / "latest.log"
if log.exists():
    nonebot.logger.success(f"已找到 {log}")
    driver = get_driver()

    @driver.on_bot_connect
    async def _(bot: Bot):

        with open(log, "r", encoding = "utf8") as fp:
            pos = fp.seek(0,2)
        while True:
            fp = open(log, "r", encoding = "utf8")
            fp.seek(pos, 0)
            line = fp.read()
            if line:
                pos = fp.seek(0,2)
                line.replace("\r\n","\n")
                line = line.strip('\n').split('\n')
                for i in range(len(line)):
                    msg_dict = log_to_dict(line[i])
                    if msg_dict["type"] == "message":
                        msg =f'【{msg_dict["nickname"]}】{msg_dict["message"]}'
                        for guild in guild_list:
                            await bot.call_api(
                                "send_guild_channel_msg",
                                guild_id = guild['guild_id'],
                                channel_id = guild['channel_id'],
                                message = msg
                                )
                            await asyncio.sleep(0.5)
            fp.close()
            await asyncio.sleep(1)
else:
    nonebot.logger.error(f"mc_log_path 地址设置错误，{log} 不存在。")

# 定义CUSTOMER权限

async def CUSTOMER(bot: Bot, event: GuildMessageEvent) -> bool:
    for guild in guild_list:
        if event.guild_id == guild["guild_id"] and event.channel_id == guild["channel_id"]:
            return True
        else:
            continue
    else:
        return False

mcr = asyncio.run(mcrcon_connect(mc_ip, mcrcon_password, mcrcon_port))

send = on_message(permission = CUSTOMER, priority = 10)

@send.handle()
async def _(bot: Bot, event: GuildMessageEvent):
    global mcr
    msg = await mc_translate(bot, event)
    try:
        mcr.command(msg)
    except (mcrcon.MCRconException, ConnectionResetError) as error:
        raise error
    except ConnectionAbortedError:
        mcr = await mcrcon_connect(mc_ip, mcrcon_password, mcrcon_port)




