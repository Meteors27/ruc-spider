# ruc-spider
## 简介
仓库目录中`RucSpider.py`是中国人民大学自动登录脚本，只需输入账号密码即可自动登录。

此脚本可用于持久化抓取各种数据，比如`Demo.py`就是一个成绩自动推送脚本。
它利用了`RucSpider.py`的登录，间隔固定时间查询成绩是否有更新，并通过手机Bark软件做到消息推送。（Bark仅有iPhone用户可用）

当然，它也可以用以制作抢课脚本等工具。譬如，你可以利用github的Actions功能，把github作为你的轻量爬虫服务器[(zhr-action-demo)](https://github.com/upupming/zhr-action-demo)；你也可以利用钉钉聊天机器人，做到实时消息推送[(zju-score-push-template)](https://github.com/PeiPei233/zju-score-push-template)……
你可以发挥你的想象力，在此repo上加以改进，并贡献在开源社区中。
欢迎fork或star本项目。

## 如何使用`Demo.py`
1. 假设你已经会`git clone`或者`Download ZIP`
2. 创建虚拟环境（非必要，可以跳过）
3. 安装依赖
   ```
   pip install -r ./requirements.txt
   ```
4. 在`Demo.py`中修改账号密码还有bark链接
5. 运行！

## 登录原理
模拟人类登录行为，向微人大`v.ruc.edu.cn`服务器发送账户密码，并通过OCR识别验证码。`RucSpider`中保持了一个`session`，可以在较长时间内利用获得的`cookie`进行接下来的网页请求。
