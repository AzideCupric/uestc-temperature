import json, os, time

# from nonebot import logger

user_json_path = os.path.join(os.path.dirname(__file__), "user.json")


def addData(user: str, Sid: str) -> bool:
    """追加新的user数据并打上时间戳"""
    nowtime = int(time.time())
    newUser = {user: {"Sid": Sid, "updateTime": nowtime}}
    try:
        if os.path.getsize(user_json_path) == 0:
            with open(user_json_path, "w+", encoding="utf-8") as ud:
                json.dump(newUser, ud, indent=4, ensure_ascii=False)

        else:
            allUser = {}

            with open(user_json_path, "r", encoding="utf-8") as ud_load:
                allUser:dict = json.load(ud_load)

            allUser.update(newUser)

            with open(user_json_path, "w", encoding="utf-8") as ud_write:
                json.dump(allUser, ud_write, indent=4, ensure_ascii=False)

    except Exception as e:
        # logger.error(repr(e))
        return False
    else:
        return True


def loadData(user: str) -> dict:
    '''
    #### 按照所记录的user查找数据 返回字典{Sid,updateTime}
    #### 查找失败则返回'Sid':'err-404','date':0
    '''
    with open(user_json_path, "r", encoding="utf-8") as ud_load:
        allUser = json.load(ud_load)
    try:
        getUser = allUser[user]
    except Exception as e:
        # logger.error(repr(e))
        return {'Sid':'err-404','date':0}
    else:
        return getUser


if __name__ == "__main__":
    """test functions"""
    user = input("input user name:")
    sid = input("input sid:")
    result = addData(user, sid)
    print(f"result:{result}")
    test = loadData(input("who:"))
    print(test)
    print(
        test["Sid"]
        + ("\n"
        + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(test["updateTime"]))
        if test["Sid"]!='err-404' else '')
    )
