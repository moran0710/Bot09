import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from time import time
import os

nonebot.init(
    start_time=time(),
    command_start={"/"},
    command_sep={".", " "},
    tarot_path=os.path.join(".", "bot09", "tarot", "resource"),
    fortune_path=os.path.join(".", "bot09", "fortune", "resource")
)

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo')

nonebot.load_from_toml("pyproject.toml")


if __name__ == "__main__":
    nonebot.run()
