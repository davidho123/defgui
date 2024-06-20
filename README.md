## 一、前言
本模块灵感来源于magicgui，感谢作者
本模块与magicgui的区别：
- 本模块主要基于tkinter，以及python标准库中的typing、ctypes。不需要安装pyside等其他第三方依赖。
- 本模块本着简易使用的原则，只有一个装饰器函数，没有其他参数设置
- 生成的输出组件与返回值数量一致

## 二、功能
  函数装饰器
- 1、可以根据函数的参数，设置输入组件
- 2、根据函数的返回值，设置输出组件
- 3、run按钮运行函数，并输出结果
- 4、tkinter进行了DPI的适配，界面不会显示模糊

## 三、使用方法
pip install defgui

直接在函数上加上装饰器就可以使用
### 注意：
- 1、函数的参数需要带类型标识，否则报错
- 2、类型标识目前支持：int、float、str、List[str]

```python
from defgui import defgui
from typing import List

@defgui
def example_function(a: int, b: float,c: str,d: List[str])-> tuple:
	"""Example function that returns a tuple of four values."""
	return a + 1, b + 1,"返回字符串：%s"%(c),d

# 运行函数
example_function()
```

![png](result.png)