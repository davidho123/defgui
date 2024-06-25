import streamlit as st
from inspect import signature , _empty as inspect_empty
import datetime

def input_component(param, func_name, default=None):
    
    key = f"{func_name}_{param.name}"
    if param.annotation == int:
        if default is None:
            default = 0
        return st.number_input(param.name, step=1, key=key, value=default)
    elif param.annotation == float:
        if default is None:
            default = 0.0
        return st.number_input(param.name, step=0.1, key=key, value=default )
    elif param.annotation == str:
        if default is None:
            default = ""
        return st.text_input(param.name, key=key, value=default )
    elif param.annotation == bool:
        if default is None:
            default = False
        return st.checkbox(param.name, key=key, value=default )
    elif param.annotation == list:
        if default is None:
            default = []
        # Assuming the default value is a list of items to select from
        return st.multiselect(param.name, options=default, key=key)
    elif param.annotation == datetime.date:
        if default is None:
            default = "today"
        return st.date_input(param.name,key=key, value=default )
    else:
        return st.write(f"Unsupported type: {param.annotation}")

def defgui_streamlit(horizontal=True, col_size=None, execute=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # st.write(f"### Function: {func.__name__}")
            params = signature(func).parameters
            input_values = []
            if horizontal:
                cols = st.columns(col_size or len(params))
                col_iter = iter(cols)
            else:
                col_iter = None

            for i, (param_name, param) in enumerate(params.items()):
                if i < len(args):  # Positional arguments
                    
                    if args[i] is inspect_empty :  # 参数没有值
                        value = None
                    else:
                        value = args[i] 
                else:  # Keyword arguments
                    if  kwargs.get(param_name, param.default) is inspect_empty:  # 参数没有值
                        value = None
                    else:
                        value = kwargs.get(param_name, param.default)
                
                if horizontal:
                    with next(col_iter):
                        input_values.append(input_component(param, func.__name__, default=value))
                else:
                    input_values.append(input_component(param, func.__name__, default=value))
            if execute:
                if st.button("Execute", key=f"{func.__name__}_button"):
                    results = func(*input_values)
                    st.write(results)
                else:
                    results = None
            else:
                results = None
            return input_values, results
        return wrapper
    return decorator



if __name__ == "__main__":   
    # st.set_page_config(layout="wide")
    # st.title("Streamlit Decorator App")

    # @defgui_streamlit(horizontal=True, col_size=[1, 1, 1, 2, 2], execute=True)
    # def greet(date: datetime.date, name: str, age: int=20 , food: list=[]) -> str:
    #     return f"{date}, Hello, {name}! You are {age} years old, you like {food}"
    
    # input_values, results = greet(name="david",food=["apple", "banana"])

    # st.write(input_values[1])

    st.set_page_config(layout="wide")
    st.title("Streamlit Decorator App")

    @defgui_streamlit(horizontal=False, col_size=None, execute=False)
    def greet(date: datetime.date, name: str, age: int , food: list) -> str:
        return f"{date}, Hello, {name}! You are {age} years old, you like {food}"
    
    cols = st.columns(3)
    with cols[0]:
        greet()

    
    