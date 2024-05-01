import json
import os
from random import randint

import nonebot
from nonebot import logger
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event, Bot
from nonebot.params import CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER

data_path = os.path.join(".", "data", "bot09_mocgm", "authorization", "group_whitelist.json")

config = nonebot.get_driver().config


async def is_auth_group(event: Event) -> bool:
    """响应规则. 如果请求群号等于授权群号返回True"""
    return event.group_id == config.bot09_auth_group_id


add_authorization = on_command("添加授权", aliases={"授权"}, rule=is_auth_group)
remove_authorization = on_command("删除授权", aliases={"取消授权"}, rule=is_auth_group)
superuser_add_authorization = on_command("sudo 添加授权", aliases={"sudo 授权"}, permission=SUPERUSER,
                                         rule=is_auth_group)
superuser_remove_authorization = on_command("sudo 删除授权", aliases={"sudo 取消授权"}, permission=SUPERUSER,
                                            rule=is_auth_group)
get_all = on_command("授权列表", rule=is_auth_group, permission=SUPERUSER)


@add_authorization.handle()
async def add_authorization_func(event: Event, args: Message = CommandArg()):
    """普通用户获取09授权，只允许单用户单授权. 触发命令：/添加授权 <qgroup_id>, /授权 <qgroup_id>"""
    # 构造转发消息节点
    reply_msg = MessageSegment.reply(event.message_id)
    if group_id := args.extract_plain_text():
        with open(data_path, "r", encoding="utf8") as f:
            authorized = json.load(f)
        for user in authorized:
            if user["qq_id"] == event.user_id:
                text_msg = MessageSegment.text("授权失败！你已经领取了一个09bot！")
                break
        else:
            authorized.append({
                "qq_id": event.user_id,
                "group_id": group_id,
                "uid": len(authorized) + 1 + randint(0, 100_00000_0000)
            })
            with open(data_path, "w", encoding="utf8") as f:
                json.dump(authorized, f, indent=4)
            logger.info(f"[MoCGM] 用户{event.user_id}为群{group_id}添加了授权")

            text_msg = MessageSegment.text(f"已经添加授权~ 你是09bot的第{len(authorized)}个主人")
        result = Message([reply_msg, text_msg])
    else:
        text_msg = MessageSegment.text("你没有指定要09授权的群号哦....")
        result = Message([reply_msg, text_msg])
    await add_authorization.finish(result)


@remove_authorization.handle()
async def remove_authorization_func(event: Event):
    """用户自行取消授权. 触发命令：/删除授权 ,/取消授权"""
    # 构造转发消息节点
    reply_msg = MessageSegment.reply(event.message_id)
    with open(data_path, "r", encoding="utf8") as f:
        authorized = json.load(f)
    for user in authorized:
        if user["qq_id"] == event.user_id:
            authorized.remove(user)
            text_msg = MessageSegment.text("已经移除了你的09bot授权")
            logger.info(f"[MoCGM] 用户{event.user_id}删除了自己的授权")
            with open(data_path, "w", encoding="utf8") as f:
                json.dump(authorized, f, indent=4)
            break

    else:
        text_msg = MessageSegment.text("你没有申请过09bot的授权欸")
    result = Message([reply_msg, text_msg])
    await add_authorization.finish(result)


@superuser_add_authorization.handle()
async def su_add_authorization_func(event: Event, args: Message = CommandArg()):
    """超级管理员强制添加授权."""
    # 构造转发消息节点
    reply_msg = MessageSegment.reply(event.message_id)
    if group_id := args.extract_plain_text():
        with open(data_path, "r", encoding="utf8") as f:
            authorized = json.load(f)
        authorized.append({
            "qq_id": "CREATED BY SUPERUSER",
            "group_id": group_id,
            "uid": len(authorized) + 1 + randint(0, 100_0000_0000)
        })
        with open(data_path, "w", encoding="utf8") as f:
            json.dump(authorized, f, indent=4)
        logger.info(f"[MoCGM] 超级管理员{event.user_id}为群{group_id}添加了授权")
        text_msg = MessageSegment.text("已经动用超级管理员权限添加授权，此授权只能由超级管理员指定授权id或群号来删除")
    else:
        text_msg = MessageSegment.text("没有提供群号参数")
    result = Message([reply_msg, text_msg])
    await add_authorization.finish(result)


@superuser_remove_authorization.got("args", prompt="请在回复中指定以下参数:\n"
                                                   "参数一：查询方式，可选qgourp_id[代号为1], 用户qq号[代号为2], 授权id[代号为3]\n"
                                                   "参数二：查询的数据\n"
                                                   "参数一直接输入代号，两个参数用空格隔开")
async def su_remove_authorization_func(event: Event, args: str = ArgPlainText()):
    args = args.split()
    # 构造转发消息节点
    reply_msg = MessageSegment.reply(event.message_id)
    with open(data_path, "r", encoding="utf8") as f:
        authorized = json.load(f)
    if len(args) == 2:
        if args[0] == "1":
            search_mode = "group_id"
        elif args[0] == "2":
            search_mode = "qq_id"
        elif args[0] == "3":
            search_mode = "uid"
        else:
            text_msg = MessageSegment.text("出现错误， 你指定的查询方式不合法")
            result = Message([reply_msg, text_msg])
            await remove_authorization.finish(result)

        for user in authorized:
            if str(user[search_mode]) == args[1]:
                authorized.remove(user)
                logger.info(f"[MoCGM] 超级管理员{event.user_id}删除了{user[search_mode]}的授权")
                text_msg = MessageSegment.text(f"已经强制删除了{search_mode}为{user[search_mode]}的授权")
                with open(data_path, "w", encoding="utf8") as f:
                    json.dump(authorized, f, indent=4)
                break
        else:
            text_msg = MessageSegment.text(f"无法查询到这个授权")
        result = Message([reply_msg, text_msg])
        await remove_authorization.finish(result)


@get_all.handle()
async def get_all_func(bot: Bot, event: Event):
    with open(data_path, "r", encoding="utf8") as f:
        authorized = json.load(f)
    result = []
    for user in authorized:
        temp = MessageSegment(type="node", data={"name": "Bot09UserList", "uin": "3575331055", "content": [
            MessageSegment.text(f"创建者：{user['qq_id']}\n绑定群聊：{user['group_id']}\nuserid：{user['uid']}")]})
        result.append(temp)
    res_id = await bot.call_api("send_forward_msg", messages=result)
    await bot.send_group_msg(group_id=event.group_id, message=MessageSegment.forward(res_id))
