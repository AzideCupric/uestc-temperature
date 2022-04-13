from typing import Any
from nonebot.plugin import on_command
from nonebot.params import ArgStr, CommandArg
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot import logger
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER

from .upload import Reporter
from .userData import delUser, listUser, updateData, loadData

from datetime import datetime, timedelta, timezone
import re

tz_utc_8 = timezone(timedelta(hours=8))

temperature = on_command("体温上报", rule=to_me())


@temperature.handle()
async def upload_temperature(user: Message = CommandArg()):
    if not user:
        logger.info("接收到空的用户名 已拒绝")
        await updateID.finish(Message("请在 体温上报 命令后加上需要更新的用户名\n例：体温上报 kaltsit"))
    logger.debug(f"Get user:{user}")
    user_data = loadData(str(user))
    if user_data["Sid"] == "err-404":
        msg = f"不存在用户：{user}\n请使用 更新id 命令添加"
    else:
        logger.info(f"Get user session id:{user_data['Sid']}")
        reporter = Reporter(user_data["Sid"])
        await temperature.send(Message(f"即将填报用户:{user}"))
        result, state = reporter.run()
        if state == "无效Session id":
            timeStamp = datetime.fromtimestamp(user_data["updateTime"], tz_utc_8)
            timeStr = timeStamp.strftime("%Y-%m-%d %H:%M:%S")
            msg = f"用户：{user}\n无效的Session id:\n{user_data['Sid']}\n上次更新时间为{timeStr}\n请发送 更新id 命令进行更新"
        else:
            msg = f"填报状态：{state}\n" + ("请自行手动填报" if not result else "")
    logger.info(msg)
    await temperature.finish(Message(msg))


updateID = on_command("更新id", rule=to_me())


@updateID.handle()
async def get_user_name(state: T_State, user_name: Message = CommandArg()):
    if not user_name:
        logger.info("接收到空的用户名 已拒绝")
        await updateID.finish(Message("请在 更新ID 命令后加上需要更新的用户名\n例：更新id amiya"))
    logger.debug(f"get name:{user_name}")
    user = loadData(str(user_name))
    if user["Sid"] == "err-404":
        await updateID.send(
            Message(f"不存在的用户：{user_name},继续发送Session Id将自动添加该用户\n或者发送 取消 中止")
        )
    else:
        timeStamp = datetime.fromtimestamp(user["updateTime"], tz_utc_8)
        timeStr = timeStamp.strftime("%Y-%m-%d %H:%M:%S")
        Sid = user["Sid"]
        await updateID.send(Message(f"{user_name}\nSession Id:{Sid}\n上次更新时间:{timeStr}"))
    state["update_user_name"] = user_name


@updateID.got("session_id", "含有新的成电智慧学工Session Id链接：")
async def update_id(state: T_State, session_id: str = ArgStr()):
    if session_id == "取消":
        await updateID.finish(Message("已中止更新"))
    pattern = re.compile(r"[A-Za-z0-9]{8}(-[A-Za-z0-9]{4}){3}-[A-Za-z0-9]{12}")
    re_result = pattern.search(session_id)
    if not re_result:
        logger.info(f"reject {session_id}")
        await updateID.reject(Message("输入的数据不满足SessionId格式！请检查后再次输入"))
    session_id = re_result.group(0)
    logger.debug(f"get id:{session_id}")
    update_user_name = str(state["update_user_name"])
    status = updateData(update_user_name, session_id)
    assert loadData(update_user_name)["Sid"] == session_id
    await updateID.send(Message(f"更新情况:{update_user_name} {status}"))


listAllUser = on_command("用户列表", rule=to_me(), permission=SUPERUSER)


@listAllUser.handle()
async def list_all_user():
    try:
        user_data_list:list[tuple[str,dict[str,Any]]]=listUser()
        assert user_data_list
    except:
        await listAllUser.finish(Message("尚未储存任何用户数据"))
    else:
        msgs='当前已添加用户:\n'
        for idx,user_box in enumerate(user_data_list,1):
            user_name=user_box[0]
            user_data=user_box[1]
            user_sid=user_data["Sid"]
            user_updateTime=user_data["updateTime"]
            msg=f"{idx}-{user_name}\n--{user_sid}\n--{user_updateTime}\n"
            msgs+=msg
        await listAllUser.finish(Message(msgs))

    
delData=on_command("删除用户",rule=to_me(),permission=SUPERUSER)

@delData.handle()
async def del_user(user:Message=CommandArg()):
    if not user:
        await delData.finish(Message("未指定需要删除的用户名，请重新输入"))
    user=str(user)
    try:
        del_info=delUser(user)
        assert del_info
    except Exception as e:
        await delData.finish(f"删除{user}失败{repr(e)}")
    else:
        sid=del_info['Sid']
        await delData.finish(f"删除{user}\n{sid}\n成功")

