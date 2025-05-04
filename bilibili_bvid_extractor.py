import json
import re

# 读取输入文件内容
with open('input.txt', 'r', encoding='utf-8') as f:
    raw_content = f.read().strip()

# ========== 修复JSON格式 ==========
# 1. 包裹方括号（如果缺少）
if not raw_content.startswith('['):
    raw_content = '[' + raw_content
if not raw_content.endswith(']'):
    raw_content += ']'

# 2. 去除最后一个元素后的多余逗号
fixed_content = re.sub(r',\s*\]$', ']', raw_content)

# ========== 解析JSON ==========
try:
    data = json.loads(fixed_content)
except json.JSONDecodeError as e:
    print(f"JSON解析失败，请检查格式: {str(e)}")
    exit()

# ========== 提取bvid ==========
bvid_list = []
for item in data:
    if isinstance(item, dict) and "bvid" in item:
        bvid_list.append(item["bvid"])
    else:
        print(f"警告：跳过无效条目 - {str(item)[:50]}...")

# ========== 写入输出文件 ==========
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(bvid_list))

print(f"成功提取 {len(bvid_list)} 个bvid到output.txt")