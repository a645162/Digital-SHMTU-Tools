# 上海海事大学 账单工具 v1.0

上海海事大学 账单工具 v1.0

# 说明

由于我([Haomin Kong](https://github.com/a645162))
开发了一个上海海事大学统一认证平台登录+验证码识别工具
([SHMTU_CAS](https://github.com/a645162/SHMTU_CAS))
能够只输入学号+密码就可以自动获取账单，无需手动输入验证码，
这就让实时获取账单成为可能，并且当检测到出现新的消费记录可以进行提醒，

因此我将不会继续维护此项目。

**画个饼：**

准备使用Qt6 + C++重写一个跨平台的桌面版工具(不仅仅是账单分析)。

[a645162/SHMTU-Terminal-Qt](https://github.com/a645162/SHMTU-Terminal-Qt)

已经新建文件夹了嗷！！！

# 工具(功能)列表

- 统一身份认证登录(需要手动打码)
- 校园卡消费清单导出工具
- 校园卡消费分析工具

# 工具介绍

## 消费清单导出工具

您登录(您只需要手动输入验证码)之后可以自动爬取您的消费清单，并且导出为csv文件。

可以用Excel/WPS直接打开！

### 安装要求

```
selenium>=4.0.0
webdriver_manager>=4.0.0
```

程序需要 selenium 分析网页，
需要webdriver_manager自动获取webdriver！

### 使用说明

1. 安装依赖
2. 请复制`template/shmtu_num_pwd.txt`到`template/shmtu_num_pwd.ini`
3. 请修改`template/shmtu_num_pwd.ini`中内容。
4. 运行`main.py`，输入验证码，等待程序自动运行

## 校园卡消费分析工具

请参考`BillAnalysis`目录中的实现。

### 支持的功能

- 对账单进行分类
- 合并连续地洗浴记录(比如中途拔卡暂停)
- 食堂用餐时段显示
- 食堂用餐地点显示

## 切换浏览器

将下面两行代码切换为其他浏览器，如Edge或者Firefox(GeckoDriver)

```python
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
```

### 声明！

本项目启动于 2023年10月6日 ，由于我也就是2023年9月9日才来，
所以，有很多消费类型我没体验过。欢迎反馈！
肯定有程序识别不出来的项目！

### 项目缺点

- 文档不完整
- 使用Selenium，需要安装WebDriver
- 使用Selenium4可能因为网络问题无法下载WebDriver
- 需要手动打码
- Python使用门槛高

因此，我决定重写一个新版！
