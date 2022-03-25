from nonebot.plugin import on_command
from nonebot.params import ArgStr, CommandArg
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot import logger
from nonebot.typing import T_State

from .upload import Reporter
from .userData import updateData, loadData

import time
import re

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


updateID = on_command("更新id", rule=to_me())


@updateID.handle()
async def get_user_name(state: T_State, user_name: str = CommandArg()):
    logger.info(f"get name:{user_name}")
    user = loadData(user_name)
    if user["Sid"] == "err-404":
        await updateID.send(
            Message(f"不存在的用户：{user_name},继续发送Session Id将自动添加该用户\n或者发送 取消 中止")
        )
    else:
        TimeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user["updateTime"]))
        Sid = user["Sid"]
        await updateID.send(
            Message(f"{user_name}\n上次更新Session Id:{Sid}\n的时间为{TimeStr}")
        )
    state["update_user_name"] = user_name


@updateID.got("session_id", "新的成电智慧学工Session Id：")
async def update_id(state: T_State, session_id: str = ArgStr()):
    if session_id == "取消":
        await updateID.finish(Message("已中止更新"))
    pattern = re.compile(r'^[A-Za-z0-9]{8}(-[A-Za-z0-9]{4}){3}-[A-Za-z0-9]{12}')
    re_result=pattern.match(session_id)
    if not re_result:
        logger.info(f"reject {session_id}")
        await updateID.reject(Message("输入的数据不满足SessionId格式！请检查后再次输入"))
    logger.info(f"get id:{session_id}")
    update_user_name = state["update_user_name"]
    status = updateData(update_user_name, session_id)
    assert loadData(update_user_name)["Sid"] == session_id
    await updateID.send(Message(f"更新情况:{update_user_name} {status}"))
