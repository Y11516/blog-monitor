import json
import requests
import os
from datetime import datetime

# --- 1. 靶场关键词映射表 ---
# 只要文件路径里包含这些关键词，就归入对应的靶场
# --- 配置所有靶场的识别关键词 ---
TARGETS_CONFIG = {
    "Bugku": ["bugku"],
    # 给 CTFHub 增加了 "web-" 和 "webf-"，因为何同学的命名习惯是 web-xxx
    "CTFHub": ["ctfhub", "ctf_hub", "web-"], 
    "Pikachu": ["pikachu"],
    "SQLi-Labs": ["sqli-labs", "sqli_labs", "sqllibs", "less-", "sqli"],
    "Upload-Labs": ["upload-labs", "upload_labs", "uploadlabs", "pass-"],
    "DVWA": ["dvwa"],
    "Burp-Labs": ["burp-labs", "burp_labs", "burplabs"],
    "RCE-Labs": ["rce-labs", "rce_labs", "rcelabs", "rce"],
    "单点靶场": ["single", "单点"] 
}
# --- 2. 同学名单（精简版） ---
BLOGS_CONFIG = [
    {"name": "魏紫钰", "repo": "Y11516/Y11516.github.io"},
    {"name": "郭梓文", "repo": "gz2008/task01"},
    {"name": "王海岩", "repo": "why-ww/why-ww.github.io"},
    {"name": "何芊宏", "repo": "heqianhong1114/myblog"},
    {"name": "王冠壹", "repo": "wgy0828/wgy0828"},
    {"name": "张紫陌", "repo": "m02142008/m02142008.github.io"},
    {"name": "刘璧瑞", "repo": "12128848/12128848.github.io"},
    {"name": "刘欣赢", "repo": "eclair-tracy/eclair-tracy.github.io"},
    {"name": "刘家怡", "repo": "gysbfff/gysbfff.github.io"}
]

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_student_lab_counts(repo):
    """获取一个同学所有靶场的文章数量"""
    # 初始化全为 0
    counts = {lab: 0 for lab in LABS_MAPPING.keys()}
    if not repo: return counts
        
    url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            # 必须是 .md 或 .html 文件
            if not (path.endswith('.md') or path.endswith('.html')): continue
            
            # 排除一些明显的非文章页面
            if any(x in path for x in ["index", "readme", "tags", "archives"]): continue
            
            # 匹配靶场关键词
            for lab_name, keywords in LABS_MAPPING.items():
                if any(kw in path for kw in keywords):
                    counts[lab_name] += 1
                    break # 一个文件算作一个靶场，防止重复计算
                    
        return counts
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return counts

def main():
    results = []
    for blog in BLOGS_CONFIG:
        counts = get_student_lab_counts(blog["repo"])
        results.append({
            "name": blog["name"], 
            "counts": counts
        })
        # 打印日志方便排查
        print(f"{blog['name']}: {counts}")
    
    # 写入 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({
            "labs": list(LABS_MAPPING.keys()), # 把表头传过去
            "students": results, 
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
