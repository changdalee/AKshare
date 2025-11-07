from datetime import datetime

# 获取当前日期和时间
now = datetime.now()
print(f"当前时间: {now}")
print(f"格式化输出: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 分别获取日期和时间
current_date = now.date()
current_time = now.time()
print(f"当前日期: {current_date}")
print(f"当前时间: {current_time}")

current_hour = datetime.now().hour
print(f"当前小时（24小时制）: {current_hour}")

# 方法2：完整示例
now = datetime.now()
print(f"当前时间: {now}")
print(f"当前小时: {now.hour}")
print(f"当前分钟: {now.minute}")
print(f"当前秒: {now.second}")