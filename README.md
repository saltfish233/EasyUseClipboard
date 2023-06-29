# EasyUseClipboard
*易用剪贴板(EasyUseClipboard)，提供了基础剪贴板功能、收藏以及插件系统*

## 功能

### 基础剪贴板功能



![image-20230629215456605](https://raw.githubusercontent.com/saltfish233/EasyUseClipboard/main/assets/202306292155750.png)

### 收藏

![image-20230629215613298](https://raw.githubusercontent.com/saltfish233/EasyUseClipboard/main/EasyUseClipboard/assets/202306292156336.png)

![image-20230629215629386](https://raw.githubusercontent.com/saltfish233/EasyUseClipboard/main/assets/202306292156423.png)

### 插件系统

通过事件监听器给出接口即可使用自己编写的插件（未来会加入更好的事件监听系统和插件操作界面）

#### example

```pyhon
from src.tnxts.listener import _clipboard_listener
from src.tnxts.plugin import PluginMetadata

_metadata = PluginMetadata(
    name="helloworld",
    author="Tnxts",
    description="在复制时输出hello, world",
    usage="复制时自动运行"
)

def print_hello():
    print("hello, world")

_clipboard_listener.on_copy(print_hello)
```

![image-20230629215912437](https://raw.githubusercontent.com/saltfish233/EasyUseClipboard/main/assets/202306292159475.png)

![image-20230629220402491](https://raw.githubusercontent.com/saltfish233/EasyUseClipboard/main/assets/202306292204536.png)

## 技术

1. 提供剪贴板操作能力
2. 实现插件系统，可自由添加插件
3. 使用sqlalchemy兼容不同数据库
4. 封装loguru实现日志系统
5. 使用PyQt5与[PyQt-Fluent-Widget](https://www.github.com/zhiyiYo/PyQt-Fluent-Widgets)实现GUI界面

## 展望

1. 代码优化
2. 实现前后端分离
3. 兼容不同操作系统
4. 实现多端实时同步
