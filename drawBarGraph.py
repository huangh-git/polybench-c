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
upperWasmRatios = []
memsWasmRatios = []
# memsWasmIncrements = []

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
        rawWasmRatios.append(float(parts[1])/float(parts[1]) * 100)  # Convert to percentage
        storeWasmRatios.append(float(parts[2])/float(parts[1]) * 100)  # Convert to percentage
        upperWasmRatios.append(float(parts[3])/float(parts[1]) * 100)
        memsWasmRatios.append(float(parts[4])/float(parts[1]) * 100)
        # memsWasmIncrements.append((float(parts[3]) - float(parts[2]))/float(parts[1]) * 100)  # Increment and convert to percentage

def calAvg(arr, rawArr):
    # 计算性能损耗的百分比
    testArray = np.array(arr)
    rawArray = np.array(rawArr)
    test_loss = ((testArray - rawArray) / rawArray) * 100
    # 计算算术平均性能损耗
    arithmetic_mean_loss = np.mean(test_loss)
    # 计算几何平均性能损耗的倍数
    geometric_mean_multiplier = np.prod(1 + (test_loss / 100))**(1/len(test_loss))
    # 将几何平均性能损耗的倍数转换为百分比
    geometric_mean_loss = (geometric_mean_multiplier - 1) * 100
    print(f"算术平均性能损耗: {arithmetic_mean_loss}%")
    print(f"几何平均性能损耗: {geometric_mean_loss}%")

calAvg(storeWasmRatios, rawWasmRatios)
calAvg(upperWasmRatios, rawWasmRatios)
calAvg(memsWasmRatios, rawWasmRatios)

# 设置图像大小和分辨率
plt.figure(figsize=(16, 8))

# 条形的宽度
bar_width = 0.25

# 条形位置
r2 = range(len(labels))
r1 = [x - bar_width for x in r2]
r3 = [x + bar_width for x in r2]

# 创建条形
plt.bar(r1, storeWasmRatios, color='green', width=bar_width, edgecolor='white', label='Store Check Only(MemS-Wasm)')
plt.bar(r2, upperWasmRatios, color='orange', width=bar_width, edgecolor='white', label='Upper Bound Check Only(MemS-Wasm)')
# 第四列只显示增量
plt.bar(r3, memsWasmRatios, color='red', width=bar_width, edgecolor='white', label='Full Check(MemS-Wasm)')#, bottom=storeWasmRatios)
plt.axhline(y=100, color='gray', linestyle='--', label="Standard Wasm")

# 添加x轴标签
plt.xlabel('Benchmark', fontweight='bold', fontsize=12)
plt.xticks([r  for r in range(len(labels))], labels, rotation=90)
plt.ylabel('relative execution time, standard wasm is 100% (%)', fontweight='bold', fontsize=12)
plt.ylim(0, 500)  # y轴的范围

# 添加图例
plt.legend()

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('./res.png', bbox_inches='tight', dpi=300)

# 显示图像
plt.show()