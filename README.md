# BiliFavToolkit
B站复制别人公开的收藏夹到自己的收藏夹


---

文件说明

1. `fetch_bilibili_favorites.js`

• 用途：抓取B站收藏夹原始数据  

• 使用方式：

  1. 修改脚本中的`MEDIA_ID`为目标收藏夹数字ID
  2. 在Chrome浏览器控制台（F12）执行
  3. 执行完成后，复制所有控制台输出到`input.txt`

```javascript
// 示例修改位置
const MEDIA_ID = 123456789; // 修改为实际收藏夹ID
```

---

2. `bilibili_bvid_extractor.py`
• 用途：提取清洗BV号  

• 运行命令：

  ```bash
  python bilibili_bvid_extractor.py
  ```
• 输入输出：  

  `input.txt` → 原始JSON数据  
  `output.txt` → 每行一个BV号（如`BV1Ab4y1a7LK`）

---

3. `batch_add_fav.py`（核心脚本）
• 配置参数：

  ```python
  COOKIE = """浏览器获取的完整Cookie字符串"""  # 必填
  FAV_ID = "123456789"                     # 目标收藏夹数字ID
  INPUT_FILE = "output.txt"                # BV号来源
  REQUEST_DELAY = 2                        # 请求间隔(秒)
  ```

• 运行命令：

  ```bash
  python batch_add_fav.py
  ```

---

操作流程指南

第一阶段：数据准备
1. Cookie获取  
   • 登录B站 → F12打开开发者工具  

   • 网络面板 → 点击`nav`请求 → 复制Headers中的`Cookie`值


2. 收藏夹ID获取  
   打开收藏夹页面，URL格式示例：  
   `https://www.bilibili.com/medialist/detail/ml123456789`  
   → 最后数字`123456789`即为目标ID

---

第二阶段：数据采集
1. 执行JavaScript脚本  
   ```javascript
   // 在浏览器控制台粘贴并运行
   // 完成后复制所有输出内容到input.txt
   ```

2. 运行清洗脚本  
   ```bash
   python bilibili_bvid_extractor.py
   ```
   *输出文件`output.txt`会自动生成*

---

第三阶段：批量操作
1. 主脚本配置检查  
   • 验证cookie是否包含三个核心字段：  

     `DedeUserID` / `SESSDATA` / `bili_jct`

2. 执行收藏程序  
   ```bash
   python batch_add_fav.py
   ```
   *系统提示：*
   ```
   ✅ Cookie验证通过
   🕒 开始处理104个视频...
   ```

---

常见问题处理

错误：Cookie验证失败
解决办法：  
1. 重新获取Cookie（确保在登录状态下）  
2. 检查是否包含`bili_ticket`字段（某些情况需要）  
3. 确认Cookie字符串为单行格式  

异常：JSON解析错误
关键检查点：  
• `input.txt`首尾是否包含`[`和`]`  

• 最后一个JSON对象后是否有多余逗号  

• 使用在线JSON校验工具验证格式  


请求被拒绝（403错误）
处理方案：  
1. 将`REQUEST_DELAY`增加到5秒以上  
2. 检查`bili_jct`参数有效性  
3. 等待2小时后重试（解除频率限制）

---

注意事项

安全警告  
▶ Cookie信息等同于账号密码，操作完成后请立即：  
1. 清空脚本中的`COOKIE`字段  
2. 删除本地临时文件`input.txt/output.txt`  
3. 不要在公共网络传输这些文件  

性能建议
• 每1000条推荐操作耗时：  

  基础耗时 = 1000 × 2秒 = 33分钟  
  建议增加10%缓冲时间 → 总计约37分钟  
• 遇到网络波动时：  

  自动重试3次 → 仍失败则记录到日志  

---

技术支持
• Python环境需求：  

  ```bash
  pip install requests tqdm
  ```

