from nonebot import on_request, on_notice
from nonebot import require
from nonebot.adapters.onebot.v11 import GroupRequestEvent, GroupIncreaseNoticeEvent, Bot

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot import logger
import nonebot

from asyncio import sleep
from random import random
import json
import os

config = nonebot.get_driver().config

data_path = os.path.join(".", "data", "bot09_mocgm", "authorization", "group_whitelist.json")


@on_request().handle()
async def invited_request_func(bot: Bot, event: GroupRequestEvent):
    with open(data_path, "r", encoding="utf-8") as f:
        authorized = json.load(f)
    if event.sub_type == "invite":
        for authorized_group in authorized:
            if str(event.group_id) == authorized_group["group_id"]:
                await sleep(2 + random())
                await bot.set_group_add_request(flag=event.flag,
                                                sub_type="invite",
                                                approve=True)
                await bot.send_group_msg(group_id=event.group_id, message="欢迎使用09bot\n"
                                                                          f"目前版本号：>>{config.version}<<\n"
                                                                          "快速开始->/help list")
                break
        else:
            await sleep(2 + random())
            await bot.set_group_add_request(flag=event.flag,
                                            sub_type="invite",
                                            approve=False,
                                            reason="此群尚未获取09的授权,"
                                                   "你可以前往开发群798523753获取授权,"
                                                   "09授权是免费的，你只需要到开发群发送:  "
                                                   "/添加授权 <你想授权的群号>  就可以完成授权")


@on_notice().handle()
async def exit_unauthorized_group_func(bot: Bot, event: GroupIncreaseNoticeEvent):
    await sleep(5 + random())
    with open(data_path, "r", encoding="utf-8") as f:
        authorized = json.load(f)
    for authorized_group in authorized:
        if str(event.group_id) == authorized_group["group_id"]:
            '''
            await bot.send_group_msg(group_id=event.group_id, message="欢迎使用09bot\n"
                                                                      f"目前版本号：>>{config.version}<<\n"
                                                                      "快速开始->/help list")
                                                                      '''
            break
    else:
        logger.warning(f"[MoCGM] 存在未授权群组{event.group_id}强制拉群, 已经退出")
        await bot.send_group_msg(group_id=event.group_id, message="此群尚未获取09的授权\n"
                                                                  "你可以前往开发群798523753获取授权\n"
                                                                  "09授权是免费的，你只需要到开发群发送:  "
                                                                  "/添加授权 <你想授权的群号>  就可以完成授权")
        await bot.set_group_leave(group_id=event.group_id)
