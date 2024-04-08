# 上海海事大学 账单工具 v1.0(已停止维护)

**新版请移步**
[https://github.com/a645162/SHMTU-Terminal-Wails](https://github.com/a645162/SHMTU-Terminal-Wails)

# 说明

由于我([Haomin Kong](https://github.com/a645162))
开发了一个上海海事大学统一认证平台登录+验证码识别工具
([SHMTU_CAS](https://github.com/a645162/SHMTU_CAS))
能够只输入学号+密码就可以自动获取账单，无需手动输入验证码，
这就让实时获取账单成为可能，并且当检测到出现新的消费记录可以进行提醒，

因此**我将不会继续维护此项目**。

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

### 账单导出工具-使用说明

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

## 账单分析工具-使用说明(待补充)

修改`BillAnalysis/bill_analysis.py`中的
`main`函数中的`csv_path`变量以及`output_dir`变量。

- `csv_path`修改为你使用本工具导出的账单的csv文件路径。
- `output_dir`修改为要输出的目录。

```python
if __name__ == '__main__':
    csv_path = ""
    output_dir = ""
```

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

## 本系列项目

### 客户端

* Go Wails版
  [https://github.com/a645162/SHMTU-Terminal-Wails](https://github.com/a645162/SHMTU-Terminal-Wails)
* Rust Tauri版(画个饼，或许以后会做吧~)

### 服务器部署模型

[https://github.com/a645162/shmtu-cas-ocr-server](https://github.com/a645162/shmtu-cas-ocr-server)

注：这个项目为王老师的研究生课程《机器视觉》的课程设计项目，仅用作学习用途！！！

### 统一认证登录流程(数字平台+微信平台)

* Kotlin版(方便移植Android)
  [https://github.com/a645162/shmtu-cas-kotlin](https://github.com/a645162/shmtu-cas-kotlin)
* Go版(为Wails桌面客户端做准备)
  [https://github.com/a645162/shmtu-cas-go](https://github.com/a645162/shmtu-cas-go)
* Rust版(未来想做Tauri桌面客户端可能会移植)

注：这个项目为王老师的研究生课程《机器视觉》的课程设计项目，仅用作学习用途！！！

### 模型训练

神经网络图像分类模型训练

[https://github.com/a645162/shmtu-cas-ocr-model](https://github.com/a645162/shmtu-cas-ocr-model)

注：这个项目为王老师的研究生课程《机器视觉》的课程设计项目，仅用作学习用途！！！

### 模型本地部署

* Windows客户端(包括VC Win32 GUI以及C# WPF)
  [https://github.com/a645162/shmtu-cas-ocr-demo-windows](https://github.com/a645162/shmtu-cas-ocr-demo-windows)
* Qt客户端(支持Windows/macOS/Linux)
  [https://github.com/a645162/shmtu-cas-ocr-demo-qt](https://github.com/a645162/shmtu-cas-ocr-demo-qt)
* Android客户端
  [https://github.com/a645162/shmtu-cas-demo-android](https://github.com/a645162/shmtu-cas-demo-android)

注：这3个项目为王老师的研究生课程《机器视觉》的课程设计项目，仅用作学习用途！！！

### 原型测试

Python+Selenium4自动化测试数字海大平台登录流程

[https://github.com/a645162/Digital-SHMTU-Tools](https://github.com/a645162/Digital-SHMTU-Tools)

注：本项目为付老师的研究生课程《Python程序设计与开发》的课程设计项目，仅用作学习用途！！！

## 免责声明

本(系列)项目仅供学习交流使用，不得用于商业用途，如有侵权请联系作者删除。

本(系列)项目为个人开发，与上海海事大学无关，仅供学习参考，请勿用于非法用途。

本(系列)项目为孔昊旻同学的**课程设计**项目，仅用作学习用途！！！
