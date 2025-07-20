from pydantic import BaseModel, BeforeValidator
from typing import Annotated


class Config(BaseModel):
    mcrcon_password: Annotated[str, BeforeValidator(lambda v: v if isinstance(v, str) else str(v))] = "A"
    """MCRcon password"""
    mcrcon_port: int = 25575
    """MCRcon 端口"""
    mcs_log_path: str = ""
    """MC Server 日志路径"""
    mcs_group_cmd: list[str] = []
    """群触发命令，如果为空则将群聊消息全部转发至服务器。"""
    mcs_group_list: list[str] = []
    """群列表"""
    mcs_mc_cmd: list[str] = []
    """MC 触发命令，如果为空则将服务器消息全部转发至群聊。"""
    mcs_mc_broadcast: dict[str, list[str]] = {}
    """MC服务器广播列表"""
