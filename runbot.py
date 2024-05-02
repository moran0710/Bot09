import subprocess
import re
from rich.console import Console
from threading import Thread
from time import sleep


class ReStdout():
    def __init__(self, process):
        self.process = process
        is_enable = False

    def enable(self):
        self.is_enable = True
        while self.is_enable:
            output = self.process.stdout.readline()
            if output:
                print(output.strip().decode('utf-8'))
            else:
                break

    def disable(self):
        self.is_enable = False

def write_to_log(log_path, process):
    with open(log_path, 'a+') as f:
        while True:
            output = process.stdout.readline()
            output = output.strip().decode('gbk', errors='ignore')
            if output:
                f.write(output+"\n")
            else:
                break


def start_nonebot():
    process = subprocess.Popen("..\\.venv\\Scripts\\python.exe bot.py", stdout=subprocess.PIPE)
    return ReStdout(process), process


def start_lagrange():
    process = subprocess.Popen(".\\lagrange\\Lagrange.Windows.exe", stdout=subprocess.PIPE)
    return ReStdout(process), process


if __name__ == '__main__':
    console = Console()
    console.print(
        """=======================================================
    ||                  09Bot 启动器                   ||
    ||                  Powered By MoranDCCX           ||
    ||                 基于Nonebot2 开发               ||
    ||                 开发交流群：798523753           ||
    =======================================================""", style="#66ccff", justify="center")
    console.print("启动机器人中", style="#7CFC00")
    # 创建子进程
    nonebot_to_stdout, nonebot_process = start_nonebot()
    lagrange_to_stdout, lagrange_process = start_lagrange()
    # 写入日志
    Thread(target=write_to_log, args=("log\\nonebot.log", nonebot_process)).start()
    Thread(target=write_to_log, args=("log\\lagrange.log", lagrange_process)).start()
    # 显示20s的lagrange
    Thread(target=lagrange_to_stdout.enable).start()
    sleep(20)
    lagrange_to_stdout.disable()
    # 显示nonebot
    Thread(target=nonebot_to_stdout.enable).start()

