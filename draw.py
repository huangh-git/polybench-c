import matplotlib.pyplot as plt
import numpy as np

# 假设的数据和标签
# rawWasm = np.array([])  # 示例数据
# storeOnly = np.array([])  # A2总是小于A3
# memsWasm = np.array([])  # 示例数据
# fileName = []  # 对应的字符串数组

labels = []
rawWasmRatios = [] 
storeWasmRatios = []
memsWasmRatios = []
memsWasmIncrements = []

with open("result.log", 'r') as file:
    # Skip the first line
    lines = file.readlines()
    for line in lines[1:]:
        # Remove all spaces
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        parts = line.split(",")
        # print(parts)
        labels.append(parts[0].split('/')[-1])  # Extract just the last part of the path for brevity
        rawWasmRatios.append(float(parts[1]) * 100)  # Convert to percentage
        storeWasmRatios.append(float(parts[2]) * 100)  # Convert to percentage
        memsWasmRatios.append(float(parts[3]) * 100)
        memsWasmIncrements.append((float(parts[3]) - float(parts[2])) * 100)  # Increment and convert to percentage

def calAvg(arr, rawArr):
    # 计算性能损耗的百分比
    stArray = np.array(arr)
    rawArray = np.array(rawArr)
    store_loss = ((stArray - rawArray) / rawArray) * 100
    # 计算算术平均性能损耗
    arithmetic_mean_loss = np.mean(store_loss)
    # 计算几何平均性能损耗的倍数
    geometric_mean_multiplier = np.prod(1 + (store_loss / 100))**(1/len(store_loss))
    # 将几何平均性能损耗的倍数转换为百分比
    geometric_mean_loss = (geometric_mean_multiplier - 1) * 100
    print(f"算术平均性能损耗: {arithmetic_mean_loss}%")
    print(f"几何平均性能损耗: {geometric_mean_loss}%")

calAvg(storeWasmRatios, rawWasmRatios)
calAvg(memsWasmRatios, rawWasmRatios)

# 设置图像大小和分辨率
plt.figure(figsize=(10, 8))

# 条形的宽度
bar_width = 0.35

# 条形位置
r1 = range(len(labels))
r2 = [x + bar_width for x in r1]

# 创建条形
plt.bar(r1, rawWasmRatios, color='grey', width=bar_width, edgecolor='white', label='Raw Wasm Ratio')
plt.bar(r2, storeWasmRatios, color='silver', width=bar_width, edgecolor='white', label='Store Only Check Wasm Ratio')
# 第四列只显示增量
plt.bar(r2, memsWasmIncrements, color='black', width=bar_width, edgecolor='white', label='Mems Wasm Increment', bottom=storeWasmRatios)

# 添加x轴标签
plt.xlabel('Benchmark', fontweight='bold', fontsize=12)
plt.xticks([r + bar_width for r in range(len(labels))], labels, rotation=90)
plt.ylabel('Percentage (%)', fontweight='bold', fontsize=12)
plt.ylim(0, 1400)  # y轴的范围

# 添加图例
plt.legend()

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('./res.png', bbox_inches='tight')

# 显示图像
plt.show()