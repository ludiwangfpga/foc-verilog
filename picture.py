import matplotlib.pyplot as plt
from datetime import datetime

# 从文件中读取数据
data = []
timestamps = []
with open('received_data.txt', 'r') as file:  # 按照实际文件路径修改
    for line in file:
        parts = line.strip().split('Received: ')
        if len(parts) == 2:
            timestamp_str = parts[0][1:20]  # 提取时间戳部分
            value = float(parts[1])
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            timestamps.append(timestamp)
            data.append(value)

# 绘制走势图
plt.figure(figsize=(10, 6))
plt.plot(timestamps, data, marker='o')
plt.xlabel('Timestamp')
plt.ylabel('Received Data')
plt.title('Received Data Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
