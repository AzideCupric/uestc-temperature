from nonebot.plugin import on_command
from nonebot.params import ArgStr, CommandArg
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot import logger

from .upload import Reporter
from .userData import addData, loadData

import time

temperature = on_command("体温上报", rule=to_me())


@temperature.handle()
async def upload_temperature(user: str = CommandArg()):
    logger.info(f"Get user:{user}")
    user_data = loadData(user)
    if user_data["Sid"] == "err-404":
        msg = f"不存在用户：{user}\n请使用 添加填报人 命令添加"
    else:
        logger.info(f"Get user session id:{user_data['Sid']}")
        reporter = Reporter(user_data["Sid"])
        await temperature.send(Message(f"即将填报用户:{user}"))
        result, state = reporter.run()
        if state == "无效Session id":
            timeStr = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(user_data["updateTime"])
            )
            msg = f"用户：{user}\n无效的Session id:\n{user_data['Sid']}\n上次更新时间为{timeStr}\n请发送 更新id 命令进行更新"
        else:
            msg = f"填报状态：{state}\n" + ("请自行手动填报" if not result else "")
    logger.info(msg)
    await temperature.finish(Message(msg))
    """@temperature.got("session_id", "成电智慧学工Session Id：")
async def upload_temperature(session_id: str = ArgStr()):
    logger.info(f"get id:{session_id}")
    reporter = Reporter(session_id)
    await temperature.send(Message(f"已接收:{session_id}"))
    result, state = reporter.run()
    if state == '无效Session id':
        lastUpdateTime=loadData()
        msg= f"无效的Session id:\n{session_id}\n请发送 更新id 命令进行更新"
    else:
        msg = f"填报状态：{state}\n" + ("请自行手动填报" if not result else "")
    logger.info(f"{msg}")
    await temperature.finish(Message(msg))"""


updateID = on_command("更新id", rule=to_me())


@updateID.got("session_id", "成电智慧学工Session Id：")
async def update_id(session_id: str = ArgStr()):
    logger.info(f"get id:{session_id}")
