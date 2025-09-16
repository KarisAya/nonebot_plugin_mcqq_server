import re
import json
from nonebot_plugin_alconna.uniseg import UniMsg, Text, At, AtAll, Emoji, Image, Voice, Video


def translate2cmd(group: str, name: str, msg: UniMsg):
    """把信息翻译成 Minecraft 信息命令

    Args:
        group (str): 群组名称
        name (str): 昵称
        msg (UniMsg): 信息

    Returns:
        return (str | None): mc指令
    """
    data: list[dict] = [{"text": f"[{group}]{name}: ", "color": "white"}]
    for seg in msg:
        if isinstance(seg, Text):
            data.append({"text": seg.text, "color": "white"})
        elif isinstance(seg, At):
            data.append({"text": f"@{seg.target}", "color": "white"})
        elif isinstance(seg, AtAll):
            data.append({"text": "@全体成员", "color": "red"})
        elif isinstance(seg, Emoji):
            data.append({"text": seg.name or "[表情]", "color": "white"})
        elif isinstance(seg, Image):
            seg_data: dict = {"text": "[图片]", "color": "yellow"}
            if seg.url:
                seg_data["clickEvent"] = ({"action": "open_url", "value": seg.url},)
                seg_data["hoverEvent"] = {"action": "show_text", "contents": [{"text": "查看图片", "color": "white"}]}
            data.append(seg_data)
        elif isinstance(seg, Voice):
            data.append({"text": "[语音]", "color": "blue"})
        elif isinstance(seg, Video):
            seg_data: dict = {"text": "[视频]", "color": "yellow"}
            if seg.url:
                seg_data["clickEvent"] = ({"action": "open_url", "value": seg.url},)
                seg_data["hoverEvent"] = {"action": "show_text", "contents": [{"text": "查看视频", "color": "white"}]}
    if data:
        return f"tellraw @a {json.dumps(data)}"


# [19:49:44] [Server thread/INFO]: <KarisAya> 1
pattern = re.compile(r"<(.+)> (.+)")


def parse_log(loginfo: str) -> tuple[str, str] | None:
    """
    转换log信息

    Args:
        loginfo (str): 日志信息

    Returns:
        return (tuple[str, str] | None): 解析内容：(玩家名, 聊天内容)
    """
    if match := pattern.search(loginfo):
        return match.groups()  # type: ignore 这里一定是匹配的
