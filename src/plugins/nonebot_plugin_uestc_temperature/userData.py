import json, os, time

# from nonebot import logger

user_json_path = os.path.join(os.path.dirname(__file__), "user.json")


def addData(user: str, Sid: str):
    """追加新的user数据并打上时间戳"""
    nowtime = int(time.time())
    newUser = {user: {"Sid": Sid, "date": nowtime}}
    try:
        if os.path.getsize(user_json_path) == 0:
            with open(user_json_path, "w+", encoding="utf-8") as ud:
                json.dump(newUser, ud)

        else:
            allUser = {}

            with open(user_json_path, "r", encoding="utf-8") as ud_load:
                allUser = json.load(ud_load)

            allUser.update(newUser)

            with open(user_json_path, "w", encoding="utf-8") as ud_write:
                json.dump(allUser, ud_write, indent=4, ensure_ascii=False)

    except Exception as e:
        print(repr(e))
        return False
    else:
        return True


if __name__ == "__main__":
    """test functions"""
    user = input("input user name:")
    sid = input("input sid:")
    result = addData(user, sid)
    print(f"result:{result}")
