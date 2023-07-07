import requests
import base64
import ddddocr
import time
import logging
import argparse
import urllib.parse
from RucSpider import RucSpider


class JwSpider(RucSpider):
    scoreURL = "https://jw.ruc.edu.cn/resService/jwxtpt/v1/xsd/cjgl_xsxdsq/findKccjList"

    def __init__(self, username, password):
        super(JwSpider, self).__init__(username, password)
        self.__json = {
            "pyfa007id": "1",
            "jczy013id": [],
            "fxjczy005id": "",
            "cjckflag": "xsdcjck",
            "page": {
                "pageIndex": 1,
                "pageSize": 30,
                "orderBy": '[{"field":"jczy013id","sortType":"asc"}]',
                "conditions": "QZDATASOFTJddJJVIJY29uZGl0aW9uR3JvdXAlMjIlM0ElNUIlN0IlMjJsaW5rJTIyJTNBJTIyYW5kJTIyJTJDJTIyY29uZGl0aW9uJTIyJTNBJTVCJTVEJTdEyTTECTTE",
            },
        }
        self.__params = {
            "resourceCode": "XSMH0526",
            "apiCode": "jw.xsd.xsdInfo.controller.CjglKccjckController.findKccjList",
        }
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "TOKEN": "",  # to be filled
            "Accept": "application/json, text/plain, */*",
        }

    def login(self):
        RucSpider.login(self)
        self.__headers["TOKEN"] = self.sess.cookies["token"]

    def getScore(self):
        try:
            self.res = self.sess.post(
                self.scoreURL,
                headers=self.__headers,
                params=self.__params,
                json=self.__json,
            )
            json = self.res.json()
            if json["errorCode"] != "success":
                raise Exception(json["errorCode"])
        except Exception as e:
            logging.error(f"JwSpider.get_score() failed: " + str(e))
            raise e
        logging.info("JwSpider.get_score() successed")
        return self.res.json()["data"]


class Messager:
    def __init__(self, source):
        self.source = source

    def send(
        self, title, body, sound="alarm", group="gpa", level="timeSensitive", url=""
    ):
        requests.post(
            f"{self.source}/{title}/{body}",
            data={
                "sound": sound,
                "group": group,
                "level": level,
                "url": url,
            },
        )

    def sendCourseScore(self, json):
        self.send(
            json["kcname"] + " " + str(json["xf"]) + "学分",
            f'平时成绩{json["cjxm1"]} 期中成绩{json["cjxm2"]} 期末成绩{json["cjxm3"]} 最终成绩{json["zcjname1"]}',
            level="timeSensitive",
        )

    def sendGPA(self, gpaSemester, gpaAll):
        self.send(
            "GPA更新", f"本学期GPA: {gpaSemester} 总GPA: {gpaAll}", level="timeSensitive"
        )


# TODO: avoid login too many times
if __name__ == "__main__":
    logging.basicConfig(
        filename="logger.log",
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="## %Y-%m-%d %H:%M:%S",
    )

    username = "你的学号"
    password = "你的密码"
    client = "你的iPhone手机bark链接"

    spider = JwSpider(username, password)
    messager = Messager(client)
    try:
        # init
        spider.login()
        oldScore = spider.getScore()
        logging.info("initial score list: " + str([x["kcname"] for x in oldScore]))
        messager.send("RUC成绩推送开始运行", "(◍•ᴗ•◍)")
        # main loop
        while True:
            spider.login()
            newScore = spider.getScore()
            if newScore != oldScore:
                # find new score
                diff = [
                    d for d in newScore if d not in oldScore and d["kcname"] is not None
                ]
                logging.info(
                    "[main] New score found: " + str([x["kcname"] for x in diff])
                )
                # send msg
                for item in diff:
                    messager.sendCourseScore(item)
                # optional msg
                # TODO: add gpa
                # update old score
                oldScore = newScore
                # sleep for 5 minutes
            time.sleep(300)
    except Exception as e:
        messager.send("RUC成绩脚本中断", str(e))
