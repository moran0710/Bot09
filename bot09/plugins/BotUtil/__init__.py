from nonebot import on_command
import nonebot
from nonebot.plugin import get_loaded_plugins
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event
from nonebot.params import CommandArg

import psutil

import time
import platform
import subprocess

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="MoC调试工具",
    description="一个极简的bot调试工具",
    usage="/ping 机器人回回复pong!\n@bot /info 机器人会回复一系列运行信息\n（超级管理员）@bot /reboot 机器人重启\n（超级管理员）@bot /exec "
          "执行一条shell命令（高危）\n（超级管理员）@bot /stop 将bot关机（需要手动重新开启）\n （超级管理员）@bot /install <Nonebot2插件包名>：安装nb插件",
    type="application",
    homepage="None",
    supported_adapters={"~onebot.v11"},
)

config = nonebot.get_driver().config

ping = on_command("ping")
info = on_command("info", rule=to_me())
reboot = on_command("reboot", rule=to_me(), permission=SUPERUSER)
execute = on_command("exec", rule=to_me(), permission=SUPERUSER)
stop = on_command("stop", rule=to_me(), permission=SUPERUSER)
install = on_command("install", rule=to_me(), permission=SUPERUSER)
uninstall = on_command("uninstall", rule=to_me(), permission=SUPERUSER)


@ping.handle()
async def ping_func():
    """
    别看了，就是个ping
    """
    await ping.finish("pong!")


@info.handle()
async def info_func(bot: Bot):
    t = time.time()
    """
    获取运行信息
    1.操作系统和版本
    2.插件列表
    3.群聊列表
    """
    # 获取系统版本信息
    os_name = platform.system()
    os_version = platform.version()
    # 获取插件对象列表
    plugin_class_list = list(get_loaded_plugins())
    plugin_list = list()
    # 转换成插件名列表
    for plugin in plugin_class_list:
        plugin_list.append(plugin.name)
    # 获取内存利用率
    mem = psutil.virtual_memory()
    used_memory = round(float(mem.used) / 1024 / 1024 / 1024, 2)
    total_memory = round(float(mem.total) / 1024 / 1024 / 1024, 2)
    free_memory = round(float(mem.free) / 1024 / 1024 / 1024, 2)
    # 获取群信息
    gocq_group_list = await bot.call_api("get_group_list")
    group_list = list()
    for group in gocq_group_list:
        group_list.append(group["group_name"])

    # 获取服务器时间
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 获取运行时间
    total_run_time_sec = time.time() - config.start_time
    days = total_run_time_sec // 86400
    hours = (total_run_time_sec - days * 86400) // 3600
    minutes = (total_run_time_sec - days * 86400 - hours * 3600) // 60
    seconds = round((total_run_time_sec - days * 86400 - hours * 3600 - minutes * 60), 0)

    # 向bot返回信息
    await info.finish(f"凌玖bot，运行版本{config.version}"
                      f"\n作者：MoranDCCX"
                      f"\n"
                      f"\n使用操作系统:{os_name}"
                      f"\n版本{os_version}"
                      f"\nCPU利用率：{psutil.cpu_percent()}%"
                      f"\n内存利用率：{used_memory}GB已用，{total_memory}GB总计，{free_memory}GB空闲"
                      f"\n已经加载插件个数：{len(plugin_list)}"
                      f"\n已经加载的插件：{plugin_list}"
                      f"\n已经加入的群聊个数：{len(group_list)}"
                      f"\n已经加入的群聊列表{group_list}"
                      f"\n"
                      f"\n距离上次重启：{days}d {hours}h {minutes}m {seconds}s"
                      f"\n当前服务器时间：{now}"
                      f"\nbot信息返回完成，耗时{time.time() - t}sec.")


@reboot.handle()
async def reboot_func():
    from nonebot_plugin_reboot import Reloader
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await reboot.send(f"现在是{now}\n机器人将在1秒后重启")
    time.sleep(1)
    await reboot.send(f"由于nonebot的机制，无法提示重启是否成功，预计将在10s后重启成功\n请使用info命令查看运行状态")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await reboot.send(f"现在是{now}\n正在重启....")
    Reloader.reload()


@execute.handle()
async def execute_func(bot: Bot, event: Event, command: Message = CommandArg()):
    command = command.extract_plain_text()
    await execute.send(f"正在执行: \n{command}")
    result = subprocess.getstatusoutput(command)
    messages = [
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"退出代码：{result[0]}")]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"标准输出：\n{result[1]}")]
            }
        }
    ]
    res_id = await bot.call_api("send_forward_msg", messages=messages)
    await bot.send_group_msg(group_id=event.group_id, message=MessageSegment.forward(res_id))


@execute.handle()
async def execute_func(bot: Bot, event: Event, command: Message = CommandArg()):
    command = command.extract_plain_text()
    await execute.send(f"正在执行: \n{command}")
    result = subprocess.getstatusoutput(command)
    messages = [
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"退出代码：{result[0]}")]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"标准输出：\n{result[1]}")]
            }
        }
    ]
    res_id = await bot.call_api("send_forward_msg", messages=messages)
    await bot.send_group_msg(group_id=event.group_id, message=MessageSegment.forward(res_id))

@install.handle()
async def execute_func(bot: Bot, event: Event, args: Message = CommandArg()):
    from nonebot_plugin_reboot import Reloader

    plugin = args.extract_plain_text()
    await install.send(f"正在安装nonebot插件: \n{plugin}")
    messages, result = await run_nbcli(f"nb plugin install {plugin}")
    res_id = await bot.call_api("send_forward_msg", messages=messages)
    await bot.send_group_msg(group_id=event.group_id, message=MessageSegment.forward(res_id))
    if result[0] == 0:
        await install.send("安装完成，正在重启机器人")
        Reloader.reload()

@uninstall.handle()
async def execute_func(bot: Bot, event: Event, args: Message = CommandArg()):
    from nonebot_plugin_reboot import Reloader

    plugin = args.extract_plain_text()
    await install.send(f"正在卸载nonebot插件: \n{plugin}")
    messages, result = await run_nbcli(f"nb plugin uninstall {plugin} -y")
    res_id = await bot.call_api("send_forward_msg", messages=messages)
    await bot.send_group_msg(group_id=event.group_id, message=MessageSegment.forward(res_id))
    if result[0] == 0:
        await install.send("卸载完成，正在重启机器人")
        Reloader.reload()


async def run_nbcli(command):
    result = subprocess.getstatusoutput(command)
    messages = [
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text("操作结果：{0}".format("成功" if result[0] == 0 else "出现错误"))]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"退出代码：{result[0]}")]
            }
        },
        {
            "type": "node",
            "data": {
                "name": "MoCExecute",
                "uin": "3575331055",
                "content": [MessageSegment.text(f"标准输出：\n{result[1]}")]
            }
        }
    ]
    return messages, result


@stop.handle()
async def stop_():
    await stop.send("机器人将关机\n请到服务器自行开机")
    exec(exit(0))
