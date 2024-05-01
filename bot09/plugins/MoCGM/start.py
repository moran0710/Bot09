import os
from nonebot import logger
import json

def start():
    # 基本目录
    make_data_dir(os.path.join(".", "data"))
    make_data_dir(os.path.join(".", "data", "bot09_mocgm"))
    # 授权系统数据目录
    make_data_dir(os.path.join(".", "data", "bot09_mocgm", "authorization"))
    make_json_file(os.path.join(".", "data", "bot09_mocgm", "authorization", "group_whitelist.json"), [])
    logger.success("[MoCGM] MoCGM正常启动！")
    with open(os.path.join(".", "data", "bot09_mocgm", "authorization", "group_whitelist.json"), "r", encoding="utf8") as f:
        data = json.load(f)
    logger.success(f"[MoCGM] 目前白名单内群聊数量: {len(data)}")


def make_data_dir(path):
    if not os.path.exists(path):
        logger.error(f"[MoCGM] 不存在{path}！正在新建")
        os.mkdir(path)

def make_json_file(path, data: dict):
    if not os.path.exists(path):
        logger.error(f"[MoCGM] 不存在{path}！正在新建")
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)