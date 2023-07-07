import requests
import base64
import ddddocr
import urllib.parse


class RucSpider(object):
    loginURL = "https://v.ruc.edu.cn/auth/login"
    captchaURL = "https://v.ruc.edu.cn/auth/captcha"
    __maxRetry = 5

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__json = {
            "username": "ruc:" + username,
            "password": password,
            "code": "",
            "remember_me": "true",
            "redirect_uri": urllib.parse.quote(
                "http://jw.ruc.edu.cn/secService/oauthlogin"
            ),
            "captcha_id": "",
        }
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
        }
        self.__captchaID = None
        self.__captchaCode = None
        self.__res = None
        self.sess = requests.Session()

    def login(self):
        # try several times
        for i in range(self.__maxRetry):
            try:
                self.captcha()
                self.__json["code"] = self.__captchaCode
                self.__json["captcha_id"] = self.__captchaID
                self.__res = self.sess.post(
                    self.loginURL, json=self.__json, headers=self.__headers
                )
                if self.__res.status_code != 200:
                    raise Exception(self.__res.json()["error_description"])
            except Exception as e:
                continue
            return
        raise Exception(f"RucSpider.login() failed after {self.__maxRetry} times")

    def captcha(self):
        self.__res = self.sess.get(self.captchaURL, headers=self.__headers)
        # Get captcha ID
        captcha_json = self.__res.json()
        self.__captchaID = captcha_json["id"]
        # Get captcha image
        captcha_png = base64.b64decode(captcha_json["b64s"].split(",")[1])
        # OCR captcha
        ocr = ddddocr.DdddOcr()
        self.__captchaCode = ocr.classification(captcha_png)
        return self.__captchaCode
