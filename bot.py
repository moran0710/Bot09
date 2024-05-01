import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from time import time

nonebot.init(
    start_time=time(),
    superusers={"3575331055"},
    command_start={"/", ""},
    command_sep={".", " "},
)

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo')

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
