import json
import requests
import os
from datetime import datetime

# --- 在这里配置所有同学的博客信息 ---
BLOGS_CONFIG = [
    {
        "name": "魏紫钰",
        "repo": "Y11516/Y11516.github.io",
        "exclude": ["index.html", "tools.html", "about.html", "dashboard.html", "bugku.html", "ctfhub.html"] 
    },
    {
        "name": "郭梓文",
        "repo": "gz2008/task01",
        "exclude": ["index.html"] 
    },
    {
        "name": "王海岩",
        "repo": "why-ww/why-ww.github.io",
        "exclude": ["index.html"]
    },
    {
        "name": "何芊宏",
        "repo": "heqianhong1114/myblog",
        "exclude": ["index.html"]
    },
    {
        "name": "王冠壹",
        "repo": "wgy0828/wgy0828",
        "exclude": ["index.html"]
    },
    {
        "name": "张紫陌",
        "repo": "m02142008/m02142008.github.io",
        "exclude": ["index.html"]
    },
    {
        "name": "刘璧瑞",
        "repo": "12128848/12128848.github.io",
        "exclude": ["index.html"]
    },
    {
        "name": "刘欣赢",
        "repo": "eclair-tracy/eclair-tracy.github.io",
        "exclude": ["index.html"]
    },
    {
        "name": "刘家怡",
        "repo": "gysbfff/gysbfff.github.io",
        "exclude": ["index.html"]
    }
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
# 如果在 GitHub Actions 中运行，会自动读取 Token 提高请求限制
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, exclude_list):
    """通过GitHub API获取指定仓库的博客文章数量"""
    url = f"https://api.github.com/repos/{repo}/contents/"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # 如果请求失败则抛出异常
        data = response.json()
        
        if not isinstance(data, list):
            return 0
            
        # 过滤出所有HTML文件，并排除掉非博客页面
        posts = [f for f in data if f['name'].endswith('.html') and f['name'] not in exclude_list]
        return len(posts)
    except Exception as e:
        print(f"获取 {repo} 数据失败: {e}")
        return 0

def main():
    results = []
    for blog in BLOGS_CONFIG:
        count = get_blog_post_count(blog["repo"], blog["exclude"])
        results.append({
            "name": blog["name"],
            "repo": blog["repo"],
            "count": count,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"{blog['name']}: {count} 篇")
    
    # 将结果写入 data.json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
