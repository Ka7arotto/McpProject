# 在 weather.py 顶部添加
import sys, os
print(f"当前工作目录: {os.getcwd()}")
print(f"Python路径: {sys.path}")
print(f"包上下文: {__package__}")
raise SystemExit("请检查上述输出")  # 强制停止