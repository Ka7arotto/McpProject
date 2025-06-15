import requests

url = "http://127.0.0.1:8000/retrieve"
data = {"query": "膀胱癌的治疗方案是什么？"}  # 表单数据

response = requests.post(url, data=data)  # 使用 data= 而不是 json=

if response.ok:
    print("响应数据:", response.json())
else:
    print("请求失败:", response.text)