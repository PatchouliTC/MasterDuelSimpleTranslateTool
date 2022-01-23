# MasterDuel图像识别翻译命令行工具
1. 安装并进入python虚拟环境[善用搜索引擎],执行`pip install -r requirements.txt`安装相关依赖
[注意该程序仅限windows环境使用,大量引用win32接口]
2. 直接启动`master_duel_main.py`文件,根据快捷键使用相关功能
## 其他注意事项:
1. `cards.cdb`来自 [YGODataBase](https://github.com/mycard/ygopro-database),下载后将对应语言下的`cards.cdb`放入根目录替换即可
2. `card_image_check.db`是缓存的图象匹配数据库,如果遇到卡牌数据更新,请删除该文件,并来[这里](https://forum.duelistsunite.org/t/japanese-card-pics/115)下载相关卡图,<strong>一定记得下载1920x1080 (484x700)高清卡图</strong>,下载后的卡图解压到`origin_ygo_img`目录
## 封包为单可执行文件:
1. 安装pyinstaller
2. 执行`pyinstaller  .\master_duel_main.py  -F  -n MasterDuel图像翻译插件`,等待执行结束
3. 以上命令会生成单文件可执行exe,将`cards.db`,生成好的`card_image_check.db`复制到对应单文件同目录下
4. <strong>记得以管理员身份执行,否则程序将无权获取其他进程hwnd!</strong>