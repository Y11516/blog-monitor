import json
import requests
import os
from datetime import datetime

# --- 在这里配置所有同学的博客信息 ---
BLOGS_CONFIG = [
    {
        "name": "Y11516",
        "repo": "Y11516/Y11516.github.io",
        "exclude": ["index.html", "tools.html", "about.html", "dashboard.html", "bugku.html", "ctfhub.html"] # 排除非博客页面
    },
    # 以后有同学的博客，就复制上面的大括号内容，加在这里
    # {
    #     "name": "同学A",
    #     "repo": "username/repo-name",
    #     "exclude": ["index.html", "about.html"]
    # },
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, exclude_list):
    url = f"https://api.github.com/repos/{repo}/contents/"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            return 0
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
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
