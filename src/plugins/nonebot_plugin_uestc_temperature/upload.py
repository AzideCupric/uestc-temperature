import json
import os

import requests
from urllib3 import Retry

site_json_path = os.path.dirname(__file__)

class Reporter:
    '''
    上报体温信息
    '''
    def __init__(self, cookie: str) -> None:
        self.__read_sites()
        self.__init_session(cookie)

    def __read_sites(self) -> None:
        #with open(os.path.join("src", "plugins", "nonebot_plugin_uestc_temperature", "sites.json"), "r", encoding="utf-8") as fr:
        with open(os.path.join(site_json_path,"sites.json"), "r", encoding="utf-8") as fr:
            self.__sites = json.load(fr)

    def __init_session(self, cookie: str) -> None:
        self.__session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=Retry(
                total=50, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
            )
        )
        self.__session.mount("http://", adapter)
        self.__session.mount("https://", adapter)
        self.__session.cookies.update({"SESSION": cookie})
        self.__session.headers.update({"content-type": "application/json"})

    def __request(self, api: str) -> dict:
        site = self.__sites[api]
        return self.__session.request(
            method=site["method"],
            url=site["url"],
            timeout=5,
            json=site["data"],
        ).json()

    def run(self) -> tuple[bool, str]:
        status = self.__request("status")["data"]

        if status == None:
            return False, "无效Session id"
        elif status["appliedTimes"] != 0:
            return (True, "重复填报")
        elif status["schoolStatus"] == 0:
            return False,"离校期间，请自行填报或者启用离校填报功能"
            #response = self.__request("unreturned")
        elif status["schoolStatus"] == 1:
            response = self.__request("returned")
        else:
            return False, "无效状态"

        if response["data"] == True:
            return True, "成功"
        else:
            return False, "无效数据"


if __name__ == "__main__":
    cookies = os.environ.get("COOKIES")
    if cookies == None:
        raise Exception("session id not provided")
    else:
        cookies = cookies.split("#")

    results = []
    for index, cookie in enumerate(cookies):
        reporter = Reporter(cookie)
        result, message = reporter.run()
        results.append(result)
        print(f"Student {index+1}: {message}")

    if not all(results):
        exit(-1)
