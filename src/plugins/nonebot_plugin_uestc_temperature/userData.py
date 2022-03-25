import json, os
from datetime import datetime,timedelta,timezone
import time
from nonebot import logger

user_json_path = os.path.join(os.path.dirname(__file__), "user.json")


def updateData(user: str, Sid: str) -> bool:
    """追加新的user数据并打上时间戳"""
    tz_utc_8 = timezone(timedelta(hours=8))
    now = datetime.now(tz=tz_utc_8)
    nowtime = int(now.timestamp())
    newUser = {user: {"Sid": Sid, "updateTime": nowtime}}
    try:
        if os.path.getsize(user_json_path) == 0:
            with open(user_json_path, "w+", encoding="utf-8") as ud:
                json.dump(newUser, ud, indent=4, ensure_ascii=False)

        else:
            allUser:dict = {}

            with open(user_json_path, "r", encoding="utf-8") as ud_load:
                allUser:dict = json.load(ud_load)

            allUser.update(newUser)

            with open(user_json_path, "w", encoding="utf-8") as ud_write:
                json.dump(allUser, ud_write, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(repr(e))
        return False
    else:
        return True


def loadData(user: str) -> dict:
    '''
    #### 按照所记录的user查找数据 返回字典{Sid,updateTime}
    #### 查找失败则返回'Sid':'err-404','updateTime':0
    '''
    err_user={'Sid':'err-404','updateTime':0}
    if os.path.getsize(user_json_path) == 0:
        return err_user
    with open(user_json_path, "r", encoding="utf-8") as ud_load:
        allUser = json.load(ud_load)
    try:
        getUser = allUser[user]
    except Exception as e:
        logger.error(repr(e))
        return err_user
    else:
        return getUser


if __name__ == "__main__":
    """test functions 测试前请注释掉有关logger的部分"""
    user = input("input user name:")
    sid = input("input sid:")
    result = updateData(user, sid)
    print(f"result:{result}")
    test = loadData(input("who:"))
    print(test)
    print(
        test["Sid"]
        + ("\n"
        + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(test["updateTime"]))
        if test["Sid"]!='err-404' else '')
    )
