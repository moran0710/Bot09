from nonebot import on_request
import nonebot
from nonebot.adapters.onebot.v11 import Bot, FriendRequestEvent
from asyncio import sleep
from random import randint

config = nonebot.get_driver().config

request = on_request(priority=1)


@request.handle()
async def add_friend(event: FriendRequestEvent, bot: Bot):
    await sleep(2+randint(1,10)/10)
    await bot.set_friend_add_request(flag=event.flag, approve=True, remark="user_{0}".format(str(event.user_id)))
    await sleep(10+2+randint(1,10)/10)
    await request.finish(message="欢迎使用09bot\n"
                                 f"目前版本号：>>{config.version}<<\n"
                                 "快速开始->/help list",
                         user_id=event.user_id)
