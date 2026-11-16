import json
import requests
import os
from datetime import datetime

# --- 1. 配置靶场关键词 ---
LABS_MAPPING = {
    "Bugku": ["bugku"],
    "CTFHub": ["ctfhub", "ctf_hub", "ctf-web", "ctf-hub", "ctdhub"], 
    "Pikachu": ["pikachu"],
    "SQLi-Labs": ["sqli-labs", "sqli_labs", "sqllibs", "less-", "sqli"],
    "Upload-Labs": ["upload-labs", "upload_labs", "uploadlabs", "pass-"],
    "DVWA": ["dvwa"],
    "Burp-Labs": ["burp-labs", "burp_labs", "burplabs"],
    "RCE-Labs": ["rce-labs", "rce_labs", "rcelabs", "rce"],
    "单点靶场": ["single", "单点"]
}

# --- 2. 少数同学的信息配置（注意最后有中括号） ---
BLOGS_CONFIG = [
    {"name": "魏紫钰", "repo": "Y11516/Y11516.github.io", "branch": "main", "url": "https://y11516.github.io/"},
    {"name": "郭梓文", "repo": "gz2008/task01", "branch": "main", "url": "https://gz2008.github.io/task01/"},
    {"name": "王海岩", "repo": "why-ww/why-ww.github.io", "branch": "main", "url": "https://why-ww.github.io/"},
    {"name": "何芊宏", "repo": "heqianhong1114/myblog", "branch": "main", "url": "https://heqianhong1114.github.io/myblog/"},
    {"name": "贺佳琪", "repo": "cecilia-scintilla/cecilia-scintilla.github.io", "url": "https://cecilia-scintilla.github.io/", "branch": "main"},
    {"name": "张紫陌", "repo": "m02142008/m02142008.github.io", "branch": "main", "url": "https://m02142008.github.io/"},
    {"name": "李梦涵", "repo": "adelinecui/adelinecui.github.io", "url": "https://adelinecui.github.io/", "branch": "main"},
    {"name": "刘欣赢", "repo": "eclair-tracy/eclair-tracy.github.io", "branch": "main", "url": "https://eclair-tracy.github.io/"},
    {"name": "刘家怡", "repo": "gysbfff/gysbfff.github.io", "branch": "main", "url": "https://gysbfff.github.io/"},
    {"name": "刘璧瑞", "repo": "12128848/12128848.github.io", "url": "https://12128848.github.io", "branch": "main"}
]

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_student_lab_counts(repo, branch):
    counts = {lab: 0 for lab in LABS_MAPPING.keys()}
    if not repo:
        return counts
        
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            if not (path.endswith('.md') or path.endswith('.html')): continue
            if any(ex in path for ex in ["index", "readme", "tags", "categories", "archives"]): continue
            
            # 1. 按路径常规匹配
            matched = False
            for lab_name, keywords in LABS_MAPPING.items():
                if any(kw in path for kw in keywords):
                    counts[lab_name] += 1
                    matched = True
                    break
            
            # 2. 针对刘璧瑞的兜底（删除了极慢的读文件逻辑，直接用文件名判断）
            if not matched and "12128848" in repo:
                excludes = ["签到", "怎么玩", "去哪里玩", "都有哪些", "比赛里"]
                if not any(ex in path for ex in excludes):
                    counts["CTFHub"] += 1
                    
        return counts
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return counts

def main():
    results = []
    for blog in BLOGS_CONFIG:
        counts = get_student_lab_counts(blog["repo"], blog.get("branch", "main"))
        
        # ================= 👇 物理外挂（如果跑完刘璧瑞还是不对，直接解开这三行的注释） 👇 =================
        # if blog["name"] == "刘璧瑞":
        #     counts["Bugku"] = 32
        #     counts["CTFHub"] = 50
        # ==================================================================================================
        
        total = sum(counts.values())
        
        results.append({
            "name": blog["name"], 
            "repo": blog["repo"] if blog["repo"] else "未填写",
            "url": blog.get("url", ""),
            "stats": counts,
            "total": total
        })
        print(f"{blog['name']}: 总计 {total} 篇")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
