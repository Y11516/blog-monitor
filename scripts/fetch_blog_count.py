import json
import requests
import os
from datetime import datetime

# --- 1. 配置靶场关键词（修复了 LABS_MAPPING 未定义的报错） ---
# --- 1. 配置靶场关键词 ---
LABS_MAPPING = {
    "Bugku": ["bugku"],
    # 👇 加上了错别字 ctdhub
    "CTFHub": ["ctfhub", "ctf_hub", "ctf-web", "ctf-hub", "ctdhub"], 
    "Pikachu": ["pikachu"],
    "SQLi-Labs": ["sqli-labs", "sqli_labs", "sqllibs", "less-", "sqli"],
    "Upload-Labs": ["upload-labs", "upload_labs", "uploadlabs", "pass-"],
    "DVWA": ["dvwa"],
    "Burp-Labs": ["burp-labs", "burp_labs", "burplabs"],
    "RCE-Labs": ["rce-labs", "rce_labs", "rcelabs", "rce"],
    "单点靶场": ["single", "单点"]
}

# --- 2. 少数同学的信息配置 ---
# 提示：如果你这里是少数人版，只需保留你要监控的几个同学即可
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
    {"name": "刘璧瑞", "repo": "	https://12128848.github.io/", "branch": "main", "url": "https://12128848.github.io/"}
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
            
                       # 1. 先按常规匹配路径（看文件夹名或文件名有没有靶场关键字）
            matched = False
            for lab_name, keywords in LABS_MAPPING.items():
                if any(kw in path for kw in keywords):
                    counts[lab_name] += 1
                    matched = True
                    break
            
            # 2. 针对文件名没带关键词的同学（李梦涵、刘璧瑞），读取文件内容解析
            if not matched and ("adelinecui" in repo or "12128848" in repo) and (path.endswith('.md') or path.endswith('.html')):
                try:
                    raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{item['path']}"
                    raw_res = requests.get(raw_url, timeout=5)
                    # 把截取长度加大到 2000 个字符，覆盖绝大多数文章的头部和正文开头
                    content = raw_res.text[:2000].lower() 
                    
                    # 在正文里找有没有靶场的名字
                    for lab_name, keywords in LABS_MAPPING.items():
                        if any(kw in content for kw in keywords):
                            counts[lab_name] += 1
                            matched = True
                            break
                except:
                    pass
            
            # ================= 👇 核心兜底逻辑（如果正文实在找不到，也不放过） 👇 =================
            if not matched and "12128848" in repo:
                # 排除掉他写的无关注释和杂谈
                excludes = ["签到", "怎么玩", "去哪里玩", "都有哪些", "比赛里"]
                if not any(ex in path for ex in excludes):
                    # 既然他是 CTF 文章，又没匹配上别人，直接强行算作 CTFHub
                    counts["CTFHub"] += 1
            
        return counts
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return counts

def main():
    results = []
    for blog in BLOGS_CONFIG:
        counts = get_student_lab_counts(blog["repo"], blog.get("branch", "main"))
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
