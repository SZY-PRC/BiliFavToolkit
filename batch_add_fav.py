# 浏览器登录B站后F12-网络-勾选保留日志-F5刷新 找到nav 找到Cookie 全部复制粘贴到下面""" """中
# ===== 配置区 =====
COOKIE = """
//删除本行后将nav下的Cookie粘贴到此行 
""".strip().replace('\n', '')  # 确保合并为单行

FAV_ID = "1111111111"  # 目的收藏夹fid需为纯数字
INPUT_FILE = "output.txt"
REQUEST_DELAY = 2  # 请求间隔（秒），建议≥1
MAX_RETRY = 3  # 失败重试次数
# ==================

import re
import requests
import time
from tqdm import tqdm


# ------------------
# Cookie校验与构造
# ------------------
def validate_cookie(cookie_str):
    required_keys = ["DedeUserID", "SESSDATA", "bili_jct"]
    extracted = {}

    patterns = {
        "DedeUserID": r"DedeUserID=([^;]+)",
        "bili_ticket": r"bili_ticket=([^;]+)",
        "SESSDATA": r"SESSDATA=([^;]+)",
        "bili_jct": r"bili_jct=([^;]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, cookie_str)
        if match:
            extracted[key] = match.group(1)

    missing = [k for k in required_keys if k not in extracted]
    if missing:
        raise ValueError(f"缺少必要Cookie字段: {missing}")

    return extracted


try:
    cookie_data = validate_cookie(COOKIE)
    # 构造Cookie字符串
    cookie_parts = [
        f"DedeUserID={cookie_data['DedeUserID']}",
        f"SESSDATA={cookie_data['SESSDATA']}",
        f"bili_jct={cookie_data['bili_jct']}"
    ]
    if 'bili_ticket' in cookie_data:
        cookie_parts.append(f"bili_ticket={cookie_data['bili_ticket']}")
    COOKIE_STR = "; ".join(cookie_parts)
    print("✅ Cookie验证通过")
except Exception as e:
    print(f"❌ Cookie错误: {str(e)}")
    exit()

# ------------------
# 收藏夹ID校验
# ------------------
if not re.match(r"^\d+$", FAV_ID):
    print(f"❌ 收藏夹ID格式错误: {FAV_ID}")
    exit()

# ------------------
# 读取BV号列表
# ------------------
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        bvid_list = list({line.strip() for line in f if re.match(r"^BV\w+$", line.strip())})
    if not bvid_list:
        print("❌ 输入文件中未找到有效BV号")
        exit()
except FileNotFoundError:
    print(f"❌ 文件不存在: {INPUT_FILE}")
    exit()

# ------------------
# 请求配置
# ------------------
session = requests.Session()
headers = {
    "Cookie": COOKIE_STR,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/",
    "Origin": "https://www.bilibili.com"
}
api_url = "https://api.bilibili.com/x/v3/fav/resource/deal"


# ===== 新增函数 =====
def bvid_to_aid(bvid: str) -> int:
    """将 BV 号转换为视频 aid"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    response = requests.get(url, headers=headers, timeout=10)
    result = response.json()

    if result.get("code") == 0:
        return result["data"]["aid"]
    else:
        raise ValueError(f"转换失败: {result.get('message')}")


# ===== 修改后的收藏函数 =====
def add_to_fav(bvid, retry=MAX_RETRY):
    # 转换 BV → aid
    try:
        aid = bvid_to_aid(bvid)
    except Exception as e:
        return False, f"无法获取aid: {str(e)}"

    params = {
        "rid": aid,  # ← 关键修改：使用数字类型的 aid
        "type": 2,
        "add_media_ids": FAV_ID,
        "csrf": cookie_data["bili_jct"]
    }

    for _ in range(retry):
        try:
            resp = session.post(api_url, headers=headers, data=params, timeout=10)
            result = resp.json()
            if result.get("code") == 0:
                return True, "成功"
            else:
                return False, result.get("message", "未知错误")
        except Exception as e:
            last_error = str(e)
            time.sleep(2)
    return False, last_error

# ------------------
# 执行主循环
# ------------------
success = 0
failed = []
progress = tqdm(bvid_list, desc="收藏进度", unit="video")

for bvid in progress:
    # 执行收藏
    status, msg = add_to_fav(bvid)

    # 更新结果
    if status:
        success += 1
        progress.set_postfix_str(f"最新: {bvid} ✅")
    else:
        failed.append(f"{bvid} 错误: {msg}")
        progress.set_postfix_str(f"最新: {bvid} ❌")

    time.sleep(REQUEST_DELAY)

# ------------------
# 输出结果
# ------------------
print(f"\n操作完成！成功: {success}个，失败: {len(failed)}个")
if failed:
    print("\n失败详情:")
    print("\n".join(failed))