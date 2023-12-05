import matplotlib.pyplot as plt
import numpy as np

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

def calAvg(arr, rawArr, info):
    # overhead
    testArray = np.array(arr)
    rawArray = np.array(rawArr)
    test_loss = ((testArray - rawArray) / rawArray) * 100
    
    arithmetic_mean_loss = np.mean(test_loss)
    # geometric mean
    geometric_mean_multiplier = np.prod(1 + (test_loss / 100))**(1/len(test_loss))
    # n%
    geometric_mean_loss = (geometric_mean_multiplier - 1) * 100
    print(f"Arithmetic average performance loss for {info}: {arithmetic_mean_loss}%")
    print(f"Geometric average performance loss for {info}: {geometric_mean_loss}%")

calAvg(storeWasmRatios, rawWasmRatios, "store check only")
calAvg(upperWasmRatios, rawWasmRatios, "upper bound check only")
calAvg(memsWasmRatios, rawWasmRatios, "full check")

plt.figure(figsize=(16, 8))

# bar width
bar_width = 0.25

# bar position in x
r2 = range(len(labels))
r1 = [x - bar_width for x in r2]
r3 = [x + bar_width for x in r2]

# draw bar
plt.bar(r1, storeWasmRatios, color='green', width=bar_width, edgecolor='white', label='Store Check Only(MemS-Wasm)') #store only
plt.bar(r2, upperWasmRatios, color='orange', width=bar_width, edgecolor='white', label='Upper Bound Check Only(MemS-Wasm)') #upper only
plt.bar(r3, memsWasmRatios, color='red', width=bar_width, edgecolor='white', label='Full Check(MemS-Wasm)') #full check
plt.axhline(y=100, color='gray', linestyle='--', label="Standard Wasm") # line for 100%

# xlabel
plt.xlabel('Benchmark', fontweight='bold', fontsize=12)
plt.xticks([r  for r in range(len(labels))], labels, rotation=90)
plt.ylabel('relative execution time, standard wasm is 100% (%)', fontweight='bold', fontsize=12)
plt.ylim(0, 500)  # range for y

plt.legend()

plt.tight_layout()

# save
plt.savefig('./res.png', bbox_inches='tight', dpi=300)

# show
plt.show()