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
    mc_ip: str = "127.0.0.1"    # 服务器 IP
    mcrcon_password: str = "1"  # MCRcon password
    mcrcon_port: int = 25575    # MCRcon 端口
