import json
import requests
import os
from datetime import datetime

# --- 核心配置区（已加上 url 字段，用于前端点击跳转） ---
BLOGS_CONFIG = [
    {
        "name": "魏紫钰",
        "repo": "Y11516/Y11516.github.io",
        "url": "https://y11516.github.io/",
        "branch": "main",
        "include_keywords": ["writeup-", "ctfhub", "bugku"], 
        "exclude_keywords": ["index", "tools", "about", "dashboard", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "郭梓文",
        "repo": "gz2008/task01",
        "url": "https://gz2008.github.io/task01/",
        "branch": "main",
        "include_keywords": ["bugku"], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "王海岩",
        "repo": "why-ww/why-ww.github.io",
        "url": "https://why-ww.github.io/",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku", "pikachu"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "何芊宏",
        "repo": "heqianhong1114/myblog",
        "url": "https://heqianhong1114.github.io/myblog/",
        "branch": "main",
        "include_keywords": ["bugku-"], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "王冠壹",
        "repo": "wgy0828/wgy0828",
        "url": "https://wgy0828.github.io/wgy0828/",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "张紫陌",
        "repo": "m02142008/m02142008.github.io",
        "url": "https://m02142008.github.io/",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "刘璧瑞",
        "repo": "12128848/12128848.github.io",
        "url": "https://12128848.github.io/",
        "branch": "main",
        "include_keywords": [], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]
    },
    {
        "name": "刘欣赢",
        "repo": "eclair-tracy/eclair-tracy.github.io",
        "url": "https://eclair-tracy.github.io/",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "刘家怡",
        "repo": "gysbfff/gysbfff.github.io",
        "url": "https://gysbfff.github.io/",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    }
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, branch, include_keywords, exclude_keywords):
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        count = 0
        
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            if not (path.endswith('.md') or path.endswith('.html')): continue
            if any(ex in path for ex in exclude_keywords): continue
            if include_keywords:
                if not any(kw.lower() in path for kw in include_keywords): continue
                    
            count += 1
            
        return count
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return 0

def main():
    results = []
    for blog in BLOGS_CONFIG:
        count = get_blog_post_count(
            blog["repo"], blog.get("branch", "main"),
            blog.get("include_keywords", []), blog.get("exclude_keywords", [])
        )
        results.append({
            "name": blog["name"], 
            "repo": blog["repo"],
            "url": blog.get("url", ""), # 新增：将网址写入 JSON
            "count": count, 
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"{blog['name']}: {count} 篇")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
