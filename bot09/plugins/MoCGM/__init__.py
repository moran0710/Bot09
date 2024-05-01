from . import start, manage_authorization, allow_friend, new_group_manager
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="09管理器",
    description="09Bot的管理模块，带一定群管功能",
    usage="""
    1.bot会自动应答加好友请求
    2.根据已经存在的授权同意自己被拉入群
    普通用户添加授权方法：/添加授权 <群号>
    普通用户删除授权方法：/删除授权
    超级管理员强制添加授权方法"：/sudo 添加授权 <群号>
    超级管理员强制取消授权方法：/sudo 取消授权  
                            之后bot会有引导""",

    type="application",

    supported_adapters={"~onebot.v11"},)

start.start()
