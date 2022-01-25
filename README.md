# MasterDuel图像识别翻译命令行工具
1. 安装并进入python虚拟环境[善用搜索引擎],执行`pip install -r requirements.txt`安装相关依赖
[注意该程序仅限windows环境使用,大量引用win32接口]
2. 直接启动`master_duel_main.py`文件,根据快捷键使用相关功能

<strong>提供的card_image_check.db是OCG+TCG卡图指纹合成缓存库,匹配计算用时会比较久,如果希望更快可以解压`card_image_check_TCG_version_20220125.zip`中基于TCG卡图的指纹或`card_image_check_OCG_version_20220125.zip`中基于OCG卡图的指纹缓存覆盖card_image_check.db</strong>

[master_duel_manual_version.py是手动触发图像检测版本,main以及master_duel_auto_scan_version是周期触发图像检测版本]
## 其他注意事项:
1. `cards.cdb`来自 [YGODataBase](https://github.com/mycard/ygopro-database),下载后将对应语言下的`cards.cdb`放入根目录即可
2. `card_image_check.db`是缓存的图象匹配数据库,如果遇到卡牌数据更新,请删除该文件,并来[这里](https://forum.duelistsunite.org/t/japanese-card-pics/115)下载相关卡图,<strong>一定记得下载1920x1080 (484x700)高清卡图</strong>,下载后的卡图解压到`origin_ygo_img`目录[该文件夹自行建立],之后直接启动该工具,程序在检测到该数据库不存在会自行读取origin_ygo_img下全部图片并构建对应的指纹缓存
## 封包为单可执行文件:
1. 安装pyinstaller
2. 执行`pyinstaller  .\master_duel_main.py  -F  -n MasterDuel图像翻译插件`,等待执行结束
3. 以上命令会生成单文件可执行exe(dist目录下),将`cards.db`,生成好的`card_image_check.db`复制到对应单文件同目录下
4. <strong>记得以管理员身份执行,否则程序将无权获取其他进程句柄!</strong>