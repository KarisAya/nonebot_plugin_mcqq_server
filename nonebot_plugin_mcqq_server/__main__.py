import asyncio
from pathlib import Path
from nonebot import get_driver, get_bots, on_message, get_plugin_config
from nonebot.log import logger
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters import Bot
from mcrcon import MCRcon, MCRconException
from nonebot_plugin_alconna.uniseg import UniMsg, Target
from nonebot_plugin_uninfo import Session, UniSession
from .config import Config
from .utils import translate2cmd

__config__ = get_plugin_config(Config)
# MCRCON
PASSWORD = __config__.mcrcon_password
PORT = __config__.mcrcon_port
MCRCON = MCRcon("127.0.0.1", PASSWORD, PORT)


async def myrule(state: T_State, session: Session = UniSession()) -> bool:
    group_id = session.scene.id
    if group_id in __config__.mcs_group_list:
        state["group"] = session.scene.name or group_id
        state["name"] = session.user.nick or session.user.name or session.user.id
        return True
    else:
        return False


reapter = range(3)
mcrcon_disconnected: bool = True


async def handler(msg: UniMsg, state: T_State):
    cmd = translate2cmd(state["group"], state["name"], msg)
    if not cmd:
        return
    global mcrcon_disconnected, reapter
    for _ in reapter:
        try:
            if mcrcon_disconnected:
                MCRCON.connect()
                mcrcon_disconnected = False
            MCRCON.command(cmd)
            return
        except (MCRconException, ConnectionRefusedError, OSError):
            mcrcon_disconnected = True
            logger.exception("信息发送失败")


rule = Rule(myrule)
if __config__.mcs_group_cmd:
    from nonebot.rule import command

    rule = command(*set(__config__.mcs_group_cmd)) & rule


matcher = on_message(rule, priority=10)
matcher.append_handler(handler)


LOG_PATH = Path(__config__.mcs_log_path)
mc_broadcast = __config__.mcs_mc_broadcast

bots = get_bots()


async def send(target_id: str, bot: Bot, message: str):
    try:
        target = Target(id=target_id, private=False, self_id=bot.self_id)
        await target.send(message)
    except Exception as e:
        logger.error(f"{bot.self_id}发送消息失败: {e}")


if not LOG_PATH.exists():
    logger.error(f"未找到 {LOG_PATH.as_posix()}, 无法进行日志广播。")
else:
    logger.success(f"已找定位到文件 {LOG_PATH.as_posix()}")
    if "all" in mc_broadcast:

        async def broadcast(message: str):
            global bots, mc_broadcast
            try:
                bot = next(iter(bots.values()))
            except StopIteration:
                return
            await asyncio.gather(*[send(group_id, bot, message) for group_id in mc_broadcast["all"]])

    else:

        async def broadcast(message: str):
            global bots, mc_broadcast
            await asyncio.gather(
                *(
                    send(group_id, bot, message)
                    for bot_id, bot in bots.items()
                    if (group_ids := mc_broadcast.get(bot_id))
                    for group_id in group_ids
                )
            )

    if __config__.mcs_mc_cmd:
        mcs_mc_cmd = __config__.mcs_mc_cmd
        from .utils import parse_log as raw_parse_log

        def parse_log(loginfo: str):

            info = raw_parse_log(loginfo)
            if not info:
                return
            name, message = info
            global mcs_mc_cmd
            for prefix in mcs_mc_cmd:
                if message.startswith(prefix):
                    message = message[len(prefix) :]
                    break
            else:
                return
            return name, message

    else:
        from .utils import parse_log

    lisen_running = True

    async def lisen_log():
        fp = LOG_PATH.open("r", encoding="utf8")
        fp.seek(0, 2)
        global lisen_running
        while lisen_running:
            try:
                pos = fp.tell()
                lines = await asyncio.to_thread(fp.readlines)
                if not lines:
                    fp.seek(pos, 0)
                    continue
                message = ["<{}> {}".format(*info) for info in (parse_log(line.strip()) for line in lines) if info]
                if message:
                    await broadcast("\n".join(message))
            except Exception:
                logger.exception("监听发生异常。")
            finally:
                await asyncio.sleep(1)
        fp.close()

    driver = get_driver()

    task: asyncio.Task

    @driver.on_startup
    async def _():
        global task
        task = asyncio.create_task(lisen_log())

    @driver.on_shutdown
    async def _():
        global task, lisen_running
        lisen_running = False
        await task
