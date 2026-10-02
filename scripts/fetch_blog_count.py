import json
import requests
import os
from datetime import datetime

# --- 在这里配置所有同学的博客信息 ---
# 核心逻辑升级：不再只扫描根目录，而是扫描整个仓库的所有文件！
# include_keywords: 只要文件路径里包含这些词（如 "writeup", "posts", ".md"），就算作一篇文章
# exclude_keywords: 排除掉这些非文章文件（如 "index", "readme", "tags"）
BLOGS_CONFIG = [
    {
        "name": "魏紫钰",
        "repo": "Y11516/Y11516.github.io",
        "branch": "main",
        # 你自己的博客：如果你想只算以 writeup- 开头的文章，就加上 "writeup"
        # 如果想把 ctfhub.html 也算文章，就加上 "ctfhub"
        "include_keywords": ["writeup", "bugku", "ctfhub", "posts"], 
        "exclude_keywords": ["index", "tools", "about", "dashboard", "readme", "标签"]
    },
    {
        "name": "郭梓文",
        "repo": "gz2008/task01",
        "branch": "main",
        # 如果他的文章都在 posts 文件夹里，加上 "posts"，是 md 文件就加 ".md"
        "include_keywords": ["posts", "writeup", ".md"], 
        "exclude_keywords": ["index", "readme", "tags"]
    },
    {
        "name": "王海岩",
        "repo": "why-ww/why-ww.github.io",
        "branch": "main",
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "何芊宏",
        "repo": "heqianhong1114/myblog",
        "branch": "main",
        # 他页面显示有很多篇，可能文章在 _posts 或 posts 里
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "王冠壹",
        "repo": "wgy0828/wgy0828",
        "branch": "main",
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "张紫陌",
        "repo": "m02142008/m02142008.github.io",
        "branch": "main",
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "刘璧瑞",
        "repo": "12128848/12128848.github.io",
        "branch": "main",
        # 他主页有 Posts 列表，可能是 posts 文件夹下的 md
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "刘欣赢",
        "repo": "eclair-tracy/eclair-tracy.github.io",
        "branch": "main",
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    },
    {
        "name": "刘家怡",
        "repo": "gysbfff/gysbfff.github.io",
        "branch": "main",
        "include_keywords": ["posts", "writeup", ".md"],
        "exclude_keywords": ["index", "readme"]
    }
]
# --- 配置结束 ---

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_blog_post_count(repo, branch, include_keywords, exclude_keywords):
    """通过GitHub Tree API 递归获取整个仓库所有文件，然后精准过滤"""
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        count = 0
        
        for item in tree:
            if item['type'] != 'blob':  # 只要文件，不要文件夹
                continue
                
            path = item['path'].lower()
            
            # 1. 必须是 .md 或 .html 文件
            if not (path.endswith('.md') or path.endswith('.html')):
                continue
                
            # 2. 排除常见的非文章文件
            if any(ex in path for ex in ['readme', 'license', 'package.json', 'config.yml']):
                continue
                
            # 3. 必须符合 include_keywords 中的至少一个关键词
            # 如果 include_keywords 为空，则全算
            if include_keywords:
                if not any(kw.lower() in path for kw in include_keywords):
                    continue
                    
            # 4. 排除 exclude_keywords
            if any(ex.lower() in path for ex in exclude_keywords):
                continue
                
            # 5. 针对HTML的额外保护：根目录下的普通 html（如 404.html），如果没有关键词，不算文章
            if path.endswith('.html') and '/' not in path:
                if not any(k in path for k in ['writeup', 'ctf', 'bugku', 'pikachu', 'post']):
                    continue

            count += 1
            
        return count
    except requests.exceptions.Timeout:
        print(f"  [超时] 请求 {repo} 超时（15秒无响应）")
        return 0
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return 0

def main():
    results = []
    for blog in BLOGS_CONFIG:
        count = get_blog_post_count(
            blog["repo"], 
            blog.get("branch", "main"),
            blog.get("include_keywords", []),
            blog.get("exclude_keywords", [])
        )
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
