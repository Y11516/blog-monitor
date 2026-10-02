import json
import requests
import os
from datetime import datetime

# --- 在这里配置所有同学的博客信息 ---
# 根据你的截图，所有 repo 均已核对无误。
# 如果某位同学依然显示 0，说明他的文章在子文件夹里（比如 _posts），你可以尝试修改 "folder"
BLOGS_CONFIG = [
    {
        "name": "魏紫钰",
        "repo": "Y11516/Y11516.github.io",
        "folder": "", 
        "exclude": ["index.html", "tools.html", "about.html", "dashboard.html", "bugku.html", "ctfhub.html"] 
    },
    {
        "name": "郭梓文",
        "repo": "gz2008/task01", 
        "folder": "", 
        "exclude": ["index.html"] 
    },
    {
        "name": "王海岩",
        "repo": "why-ww/why-ww.github.io",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "何芊宏",
        "repo": "heqianhong1114/myblog",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "王冠壹",
        "repo": "wgy0828/wgy0828",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "张紫陌",
        "repo": "m02142008/m02142008.github.io",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "刘璧瑞",
        "repo": "12128848/12128848.github.io",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "刘欣赢",
        "repo": "eclair-tracy/eclair-tracy.github.io",
        "folder": "", 
        "exclude": ["index.html"]
    },
    {
        "name": "刘家怡",
        "repo": "gysbfff/gysbfff.github.io",
        "folder": "", 
        "exclude": ["index.html"]
    }
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, folder, exclude_list):
    """通过GitHub API获取指定仓库的博客文章数量"""
    url = f"https://api.github.com/repos/{repo}/contents/{folder}"
    try:
        # 加了 timeout=10，防止某个同学的博客不通导致卡死
        response = requests.get(url, headers=HEADERS, timeout=10) 
        response.raise_for_status() 
        data = response.json()
        
        if not isinstance(data, list):
            print(f"  [警告] {repo} 返回的不是文件列表，可能是空文件夹")
            return 0
            
        # 过滤出 .html 和 .md 结尾的文章文件，并排除非文章页面
        posts = []
        for f in data:
            name = f['name']
            if f['type'] == 'file' and (name.endswith('.html') or name.endswith('.md')):
                if name not in exclude_list:
                    posts.append(name)
                    
        return len(posts)
    except requests.exceptions.Timeout:
        print(f"  [超时] 请求 {repo} 超时（10秒无响应）")
        return 0
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return 0

def main():
    results = []
    for blog in BLOGS_CONFIG:
        count = get_blog_post_count(blog["repo"], blog.get("folder", ""), blog["exclude"])
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
