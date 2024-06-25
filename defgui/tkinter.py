import tkinter as tk
from tkinter import ttk
from typing import Callable, Any, Dict, List, Tuple
import ctypes

# dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)


def defgui_tkinter(func: Callable) -> Callable:
    """装饰器，用于创建GUI界面"""
    def wrapper(*args, **kwargs):
        # 创建主窗口
        root = tk.Tk()
        root.title(func.__name__)

        # 获取屏幕宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 存储输入组件的变量
        input_vars = {}

        # 获取函数的参数类型注解（除去返回类型）
        annotations = {k: v for k, v in func.__annotations__.items() if k != 'return'}

        # 根据函数参数创建输入组件
        for i, param in enumerate(annotations.keys()):
            label = ttk.Label(root, text=param)
            label.grid(row=i, column=0, sticky=tk.W,padx=10)

            # 根据参数类型创建不同类型的输入组件
            if annotations[param] == int:
                var = tk.IntVar()
                entry = ttk.Entry(root, textvariable=var)
            elif annotations[param] == float:
                var = tk.DoubleVar()
                entry = ttk.Entry(root, textvariable=var)
            elif annotations[param] == str:
                var = tk.StringVar()
                entry = ttk.Entry(root, textvariable=var)
            elif annotations[param] == List[str]:
                var = tk.StringVar()
                entry = ttk.Entry(root, textvariable=var)
                # 提示用户输入格式
                label.config(text=f"{param} (逗号分隔的列表)")
            else:
                raise ValueError("Unsupported type")
            

            entry.grid(row=i, column=1, sticky=(tk.W, tk.E),padx=5)
            input_vars[param] = var

        # 创建执行按钮
        execute_button = ttk.Button(root, text="run", command=lambda: execute_func(func, input_vars, root))
        execute_button.grid(row=len(annotations) + 1, columnspan=2)

        # 从输入组件获取参数值，并转换为适当的类型
        kwargs = {}
        for key, var in input_vars.items():
            if func.__annotations__[key] == List[int]:
                kwargs[key] = [int(x) for x in var.get().split(',')]
            elif func.__annotations__[key] == List[str]:
                kwargs[key] = var.get().split(',')
            else:
                kwargs[key] = var.get()

        # 调用函数并获取返回值
        result = func(**kwargs)

        # 如果result是元组
        if isinstance(result, tuple):
            for i, value in enumerate(result):
                output_label = ttk.Label(root, text=f"return {i+1}:   ")
                output_label.grid(row=len(func.__annotations__) + 2 + i, columnspan=2,padx=5)

        # 如果result不是元组
        else:
            output_label = ttk.Label(root, text=f"return:   ")
            output_label.grid(row=len(func.__annotations__) + 2, columnspan=2,padx=5)

        # 更新窗口，以便我们可以获取其宽度和高度
        root.update_idletasks()

        # 获取窗口宽度和高度
        window_width = root.winfo_width()
        window_height = root.winfo_height()

        # 计算窗口在屏幕中间的坐标
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))

        # 设置窗口的位置
        root.geometry(f"{window_width+20}x{window_height+20}+{x_coordinate}+{y_coordinate}")

        # 启动事件循环
        root.mainloop()

    return wrapper

def execute_func(func: Callable, input_vars: Dict[str, tk.Variable], root: tk.Tk):
    """执行被装饰的函数，并更新输出组件"""
    # 从输入组件获取参数值，并转换为适当的类型
    kwargs = {}
    for key, var in input_vars.items():
        if func.__annotations__[key] == List[int]:
            kwargs[key] = [int(x) for x in var.get().split(',')]
        elif func.__annotations__[key] == List[str]:
            kwargs[key] = var.get().split(',')
        else:
            kwargs[key] = var.get()

    # 调用函数并获取返回值
    result = func(**kwargs)

    # 删除旧的输出组件
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > len(func.__annotations__) + 1:
            widget.grid_forget()

    # 如果result是元组
    if isinstance(result, tuple):
        for i, value in enumerate(result):
            output_label = ttk.Label(root, text=f"return {i+1}:   {value}")
            output_label.grid(row=len(func.__annotations__) + 2 + i, columnspan=2,padx=5)

    # 如果result不是元组
    else:
        output_label = ttk.Label(root, text=f"return:   {result}")
        output_label.grid(row=len(func.__annotations__) + 2, columnspan=2,padx=5)

    return result

if __name__ == "__main__":
	#测试
    @defgui_tkinter
    def example_function(a: int, b: float,c: str,d: List[str])-> tuple:
        """Example function that returns a tuple of two numbers."""
        return a + 1, b + 1,"str:%s"%(c),d

    # 运行函数
    example_function()
