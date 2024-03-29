from pydantic import BaseModel, Extra

class Config(BaseModel, extra = Extra.ignore):
    '''
    guild_list: list = [
        {"guild_id": 0, "channel_id": 0},
        {"guild_id": 1, "channel_id": 1}
        ]
    '''
    group_list: list = []
    guild_list: list = []
    mc_log_path: str = r"D:\MinecraftServer\logs"
    mcrcon_password: str = "1"  # MCRcon password
    mcrcon_port: int = 25575    # MCRcon 端口

import nonebot

global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config.dict())

group_list = config.group_list
guild_list = config.guild_list
mc_log_path = config.mc_log_path
mcrcon_password = config.mcrcon_password
mcrcon_port = config.mcrcon_port