"""
Nonebot 2 Help Plugin
Author: XZhouQD
Since: 16 May 2021
"""
import nonebot

from .config import Config
from .handler import helper


default_start = list(nonebot.get_driver().config.command_start)[0]

# Legacy way of self registering (use custom attributes)
# Deprecated for nonebot-plugin-help 0.3.1+, prefer PluginMetadata.extra['version']
__help_version__ = '0.6.0'
# Deprecated for nonebot-plugin-help 0.3.0+, prefer PluginMetadata.name
__help_plugin_name__ = "09Bot Help Menu"
# Deprecated for nonebot-plugin-help 0.3.0+, prefer PluginMetadata.usage
__usage__ = f'''欢迎使用09Bot Help Menu
09bot可以使用的命令前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
'''

# New way of self registering (use PluginMetadata)
__plugin_meta__ = nonebot.plugin.PluginMetadata(
    name='Bot09 Help Menu',
    description='Bot09帮助插件',
    usage=f'''欢迎使用09Bot Help Menu
此Bot配置的命令前缀：{" ".join(list(nonebot.get_driver().config.command_start))}

{default_start}help  # 获取本插件帮助
{default_start}help list  # 展示已加载插件列表
{default_start}help <插件名>  # 调取目标插件帮助信息
''',
    type='application',
    homepage='https://github.com/xzhouqd/nonebot-plugin-help',
    extra={'version': '0.6.0'},
    config=Config,
)
