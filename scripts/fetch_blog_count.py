import json
import requests
import os
from datetime import datetime

# --- 配置所有靶场的识别关键词 ---
# 爬虫会根据这些词去匹配文件名或路径，包含该词就归入对应的靶场
TARGETS_CONFIG = {
    "Bugku": ["bugku"],
    "CTFHub": ["ctfhub", "ctf_hub"],
    "Pikachu": ["pikachu"],
    "SQLi-Labs": ["sqli-labs", "sqli_labs", "sqllibs", "less-", "sqli"],
    "Upload-Labs": ["upload-labs", "upload_labs", "uploadlabs", "pass-"],
    "DVWA": ["dvwa"],
    "Burp-Labs": ["burp-labs", "burp_labs", "burplabs"],
    "RCE-Labs": ["rce-labs", "rce_labs", "rcelabs", "rce"],
    "单点靶场": ["single", "单点"] # 如果文件名有特定特征，可以在这里加
}

# --- 同学配置（保留你之前的34人信息） ---
BLOGS_CONFIG = [
    {"name": "李晓峰", "repo": "yes-uisi/lxf", "branch": "main"},
    {"name": "郭梓文", "repo": "gz2008/task01", "branch": "main"},
    {"name": "刘璧瑞", "repo": "12128848/12128848.github.io", "branch": "main"},
    {"name": "周润祥", "repo": "zrx-wyx/zrx-wyx.github.io", "branch": "main"},
    {"name": "闫凯峰", "repo": "yankaifeng70-bot/yankaifeng70-bot.github.io", "branch": "main"},
    {"name": "刘欣赢", "repo": "eclair-tracy/eclair-tracy.github.io", "branch": "main"},
    {"name": "何芊宏", "repo": "heqianhong1114/myblog", "branch": "main"},
    {"name": "刘家怡", "repo": "gysbfff/gysbfff.github.io", "branch": "main"},
    {"name": "路博雄", "repo": "goldfish1232123/goldfish1232123.github.io", "branch": "main"},
    {"name": "宋疏桐", "repo": "", "branch": "main"},
    {"name": "贺佳琪", "repo": "cecilia-scintilla/cecilia-scintilla.github.io", "branch": "main"},
    {"name": "赵睿轩", "repo": "zxy-wx-007/zxy-wx-007.github.io", "branch": "main"},
    {"name": "童杰瑞", "repo": "rabit222/rabit222.github.io", "branch": "main"},
    {"name": "张宇晗", "repo": "zhangyuhan1214/zhangyuhan1214.github.io", "branch": "main"},
    {"name": "魏紫钰", "repo": "Y11516/Y11516.github.io", "branch": "main"},
    {"name": "佟奕轩", "repo": "12eternity31/12eternity31.github.io", "branch": "main"},
    {"name": "王嘉宝", "repo": "wangjiabao711815/wangjiabao711815.github.io", "branch": "main"},
    {"name": "周璟", "repo": "novaisntnova/novaisntnova.github.io", "branch": "main"},
    {"name": "张奕菲", "repo": "Makerzyf/Makerzyf.github.io", "branch": "main"},
    {"name": "李梦涵", "repo": "adelinecui/adelinecui.github.io", "branch": "main"},
    {"name": "艾小杭", "repo": "aixiaohang/aixiaohang.github.io", "branch": "main"},
    {"name": "王冠壹", "repo": "wgy0828/wgy0828", "branch": "main"},
    {"name": "王博昱", "repo": "wby071115/wby071115.github.io", "branch": "main"},
    {"name": "李昊阳", "repo": "02057/02057.github.io", "branch": "main"},
    {"name": "陈禹含", "repo": "girwoft/girwoft.github.io", "branch": "main"},
    {"name": "王允恒", "repo": "buu-yun/buu-yun.github.io", "branch": "main"},
    {"name": "彭紫宸", "repo": "pzc615156/pzc615156.github.io", "branch": "main"},
    {"name": "王鹏绮", "repo": "wpq-coder/pengqi.github.io", "branch": "main"},
    {"name": "邓博元", "repo": "buu2026sec078k/buu2026sec078k.github.io", "branch": "main"},
    {"name": "孙旌博", "repo": "xysjb1-create/xysjb1", "branch": "main"},
    {"name": "王远鹏", "repo": "xiadie174/xiadie-s-", "branch": "main"},
    {"name": "黄森豪", "repo": "", "branch": "main"},
    {"name": "张绍勇", "repo": "zhshy-chi/zhshy-chi.github.io", "branch": "main"},
    {"name": "孙家诚", "repo": "eternity33313/eternity33313.github.io", "branch": "main"}
]

HEADERS = {"Accept": "application/vnd.github.v3+json"}
if os.environ.get('GITHUB_TOKEN'):
    HEADERS["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"

def get_student_stats(repo, branch):
    """获取学生的靶场统计数据"""
    # 初始化该同学所有靶场数量为 0
    stats = {target: 0 for target in TARGETS_CONFIG.keys()}
    
    if not repo:
        return stats # 没填仓库直接返回全 0
        
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15) 
        response.raise_for_status() 
        data = response.json()
        
        tree = data.get('tree', [])
        
        for item in tree:
            if item['type'] != 'blob': continue
            path = item['path'].lower()
            
            # 必须是文章文件
            if not (path.endswith('.md') or path.endswith('.html')): continue
            # 排除非文章页面
            if any(ex in path for ex in ["index", "readme", "tags", "categories", "archives"]): continue
            
            # 判断该文件属于哪个靶场
            for target_name, keywords in TARGETS_CONFIG.items():
                if any(kw in path for kw in keywords):
                    stats[target_name] += 1
                    break # 找到一个匹配的就够了，防止重复计算
                    
        return stats
    except Exception as e:
        print(f"  [错误] 获取 {repo} 数据失败: {e}")
        return stats

def main():
    results = []
    for blog in BLOGS_CONFIG:
        stats = get_student_stats(blog["repo"], blog.get("branch", "main"))
        
        # 计算该同学的总数
        total_count = sum(stats.values())
        
        results.append({
            "name": blog["name"], 
            "repo": blog["repo"] if blog["repo"] else "未填写",
            "stats": stats,
            "total": total_count
        })
        print(f"{blog['name']}: 总计 {total_count} 篇 | 详情: {stats}")
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"blogs": results, "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
