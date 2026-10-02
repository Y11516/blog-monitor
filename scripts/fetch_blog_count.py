import json
import requests
import os
from datetime import datetime

# --- 核心配置区（请根据每个人的博客结构灵活调整） ---
# include_keywords: 【白名单】路径或文件名必须包含这些词之一，才算文章。
#                   如果是空列表 []，则代表“只要不是黑名单里的，全都算”。
# exclude_keywords: 【黑名单】路径或文件名包含这些词的，绝对不算。
BLOGS_CONFIG = [
    {
        "name": "魏紫钰",
        "repo": "Y11516/Y11516.github.io",
        "branch": "main",
        # 👇 你的博客：如果你只想统计 writeup- 开头的文章，就保留 ["writeup-"]
        # 如果你想把 ctfhub.html、bugku.html 也算作 1 篇文章，就加上它们
        "include_keywords": ["writeup-", "ctfhub", "bugku"], 
        "exclude_keywords": ["index", "tools", "about", "dashboard", "readme", "tags", "categories", "archives"]
    },
     {
        "name": "郭梓文",
        "repo": "gz2008/task01",
        "branch": "main",
        # 白名单加入 "bugku"，因为他的文章都在 bugku 文件夹里
        "include_keywords": ["bugku"], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },

    {
        "name": "王海岩",
        "repo": "why-ww/why-ww.github.io",
        "branch": "main",
        # 他显示49篇，可能里面有分类页，我们尝试限定一下
        "include_keywords": ["writeup", "posts", "ctf", "bugku", "pikachu"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "何芊宏",
        "repo": "heqianhong1114/myblog",
        "branch": "main",
        # 白名单加入 "bugku-"，这样所有 bugku- 开头的文章都能被统计
        "include_keywords": ["bugku-"], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },

    {
        "name": "王冠壹",
        "repo": "wgy0828/wgy0828",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "张紫陌",
        "repo": "m02142008/m02142008.github.io",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "刘璧瑞",
        "repo": "12128848/12128848.github.io",
        "branch": "main",
        "include_keywords": [], 
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives", "css", "js", "assets"]
    },
    {
        "name": "刘欣赢",
        "repo": "eclair-tracy/eclair-tracy.github.io",
        "branch": "main",
        "include_keywords": ["writeup", "posts", "ctf", "bugku"],
        "exclude_keywords": ["index", "readme", "tags", "categories", "archives"]
    },
    {
        "name": "刘家怡",
        "repo": "gysbfff/gysbfff.github.io",
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
            
            # 必须是文章文件类型
            if not (path.endswith('.md') or path.endswith('.html')): continue
            
            # 1. 命中黑名单（非文章文件），直接跳过
            if any(ex in path for ex in exclude_keywords): continue
                
            # 2. 如果设置了白名单，必须命中白名单才计算
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
            "name": blog["name"], "repo": blog["repo"],
            "count": count, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"{blog['name']}: {count} 篇")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
