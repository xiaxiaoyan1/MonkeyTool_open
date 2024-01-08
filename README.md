# MonkeyTool_open
MonkeyTool
一、操作步骤
    1、设备连接，需要先连接adb设备
    2、根据设备列表选择对应设备
    3、选择测试包名，第三步选择设置之后，会拉取所有包列表（支持模糊搜索）
    4、事件比例总和必须为100%
    4、选择日志和性能excel存放路径（monkey日志和设备手机CPU，内存数据）
    6、点击启动Monkey测试
    7、测试完成后，monkey运行状态为monkey运行完成

二、日志&报告说明
    1、过程日志：console日志会在电脑C盘根目录
    2、报告：会在选择的存放路径下生成monkey日志文件，筛选过后的错误日志文件，设备性能数据excel

三、框架结构
monkey_main.py(windows) and monkey_MacTool.py(windows): 主入口文件
device_data.py: 获取手机基本信息以及adb基本命令封装
consoleLog.py: 封装logger类,方便后续分析问题
log_analysis.py：日志分析：
performance.py： 将设备性能数据保存excel并生成图标
search_Combobox： 下拉框增加搜索功能方法封装
send_dingtalk: 发送钉钉方法封装

打包命令：
pyinstaller --onefile  --hidden-import pandas --windowed monkey_main.py
