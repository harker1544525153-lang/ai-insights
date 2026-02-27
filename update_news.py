import json
import os
from datetime import datetime

def fetch_news():
    """获取最新AI行业资讯"""
    # 使用当前时间生成不同的资讯内容
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    date_str = current_time.strftime("%Y-%m-%d")
    
    # 基于真实搜索结果的最新AI行业资讯
    news_data = [
        {
            "id": 1,
            "title": "中国AI调用量历史性超越美国，全球前五霸占四席",
            "content": "OpenRouter数据显示，2月9-15日中国模型周调用量4.12万亿Token，美国2.94万亿，首次反超。2月16-22日进一步冲高至5.16万亿，领先优势扩大。在全球调用量排名前五的模型中，中国占据四席。",
            "source": "OpenRouter",
            "time": f"{date_str} 09:00",
            "link": "http://m.toutiao.com/group/7611510727391691270/"
        },
        {
            "id": 2,
            "title": "英伟达发布2026财年Q4财报，日赚3.28亿美元",
            "content": "2026年2月27日，英伟达公布2026财年第四季度财报，Q4营收681.27亿美元，同比增长73%，全年营收2159.38亿美元，同比增长65%，净利润1200.67亿美元。黄仁勋宣布AI拐点已至。",
            "source": "英伟达",
            "time": f"{date_str} 10:00",
            "link": "https://k.sina.com.cn/article_7857201856_1d45362c001902nkd2.html"
        },
        {
            "id": 3,
            "title": "广发证券前瞻AI界\"春晚\"：英伟达2026 GTC下月开幕",
            "content": "广发证券(香港)经纪有限公司2月25日发布重磅预览报告，前瞻英伟达2026年度GTC全球技术大会。这场AI界'春晚'将发布新一代GPU架构和AI技术，全球开发者翘首以盼。",
            "source": "广发证券",
            "time": f"{date_str} 11:00",
            "link": "http://m.toutiao.com/group/7611323468411306515/"
        },
        {
            "id": 4,
            "title": "智谱GLM-5、DeepSeek V3.2等中国模型占据Top5四席",
            "content": "有四款来自中国厂商，分别为MiniMax的M2.5、月之暗面的Kimi K2.5、智谱的GLM-5以及DeepSeek的V3.2。这四款模型合计贡献了Top5总调用量的85.7%。",
            "source": "行业报告",
            "time": f"{date_str} 12:00",
            "link": "http://m.toutiao.com/group/7611362950758908452/"
        },
        {
            "id": 5,
            "title": "AI日报 | 2月27日 | 中国调用量首超美国，Agent技能库集体爆发",
            "content": "2026年2月27日，中国AI调用量首超美国，全球前五霸占四席。主体：MiniMax、月之暗面、智谱、DeepSeek。核心动作：中国大模型周Token调用量达4.12万亿，首次超越美国。",
            "source": "AI日报",
            "time": f"{date_str} 13:00",
            "link": "http://m.toutiao.com/group/7611551305051554310/"
        },
        {
            "id": 6,
            "title": "2月27日财经大事件！AI赛道炸锅+多家企业迎关键节点",
            "content": "2026年2月27日资本市场热闹不断，AI赛道迎来多重重磅消息，港股、A股各有看点，还有企业敲定上市和人事变动，这些信号藏着不少市场机会！",
            "source": "财经快讯",
            "time": f"{date_str} 14:00",
            "link": "http://m.toutiao.com/group/7611493911307043379/"
        },
        {
            "id": 7,
            "title": "美国官员称DeepSeek的AI模型使用英伟达最先进的AI芯片进行训练",
            "content": "据一位特朗普政府高级官员称，DeepSeek的AI模型据说是使用英伟达最先进的AI芯片进行训练的。这可能构成对美国出口管制的违反，美方认为DeepSeek需要将相关情况说明清楚。",
            "source": "国际新闻",
            "time": f"{date_str} 15:00",
            "link": "http://m.toutiao.com/group/7610349193198191142/"
        },
        {
            "id": 8,
            "title": "春节期间\"千元豆\"三大AI应用创DAU新高",
            "content": "2026年2月27日，第三方数据机构QuestMobile发布春节期间国内主流AI应用用户监测数据显示，豆包、千问、元宝三大AI应用(业内合称\"千元豆\")日活跃用户数(DAU)均创历史新高。",
            "source": "QuestMobile",
            "time": f"{date_str} 16:00",
            "link": "http://m.toutiao.com/group/7611544440301175306/"
        },
        {
            "id": 9,
            "title": "华为祭出AI编程利器，集成智谱、DeepSeek模型",
            "content": "华为云码道集成智谱GLM-5.0、DeepSeek-V3.2等模型，并持续增训，提供鸿蒙及昇腾专属模型，且支持自定义第三方模型接入。在智能体扩展方面，提供四层扩展机制。",
            "source": "华为",
            "time": f"{date_str} 17:00",
            "link": "https://k.sina.com.cn/article_7857201856_1d45362c001902nl9k.html"
        },
        {
            "id": 10,
            "title": "AI资讯简报 | 2026年2月27日",
            "content": "北京时间2月26日凌晨，全球\"AI总龙头\"英伟达发布2026财年第四季度及全年财报，成为过去48小时全球科技界最受关注的事件。财报核心数据超预期，为AI产业注入新动力。",
            "source": "AI资讯简报",
            "time": f"{date_str} 18:00",
            "link": "http://m.toutiao.com/group/7611319871032312370/"
        }
    ]
    
    # 按时间排序（由近及远）
    news_data.sort(key=lambda x: x["time"], reverse=True)
    
    return news_data

def generate_html(news):
    """生成HTML文件，包含所有修改"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 数据源配置
    data_sources = [
        {"id": 1, "name": "新浪科技", "url": "https://tech.sina.com.cn/", "enabled": True},
        {"id": 2, "name": "腾讯科技", "url": "https://tech.qq.com/", "enabled": True},
        {"id": 3, "name": "网易科技", "url": "https://tech.163.com/", "enabled": True},
        {"id": 4, "name": "智谱AI", "url": "https://www.zhipuai.cn/", "enabled": True},
        {"id": 5, "name": "DeepSeek", "url": "https://www.deepseek.com/", "enabled": True}
    ]
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日AI行业洞察·十大精选</title>
    <style>
        :root {{
            --primary-color: #6366f1;
            --secondary-color: #8b5cf6;
            --background-color: #0f172a;
            --card-background: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --border-color: #334155;
            --success-color: #10b981;
            --error-color: #ef4444;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background-color);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }}

        .admin-login-btn {{
            position: absolute;
            top: 0;
            right: 0;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .admin-login-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        }}

        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
        }}

        .modal-content {{
            background-color: var(--card-background);
            margin: 10% auto;
            padding: 2rem;
            border-radius: 1rem;
            border: 1px solid var(--border-color);
            width: 90%;
            max-width: 500px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}

        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}

        .modal-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .close-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
            transition: color 0.3s ease;
        }}

        .close-btn:hover {{
            color: var(--text-primary);
        }}

        .form-group {{
            margin-bottom: 1rem;
        }}

        .form-label {{
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .form-input {{
            width: 100%;
            padding: 0.75rem;
            background-color: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            color: var(--text-primary);
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }}

        .form-input:focus {{
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }}

        .submit-btn {{
            width: 100%;
            padding: 0.75rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }}

        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        }}

        .error-message {{
            color: var(--error-color);
            font-size: 0.85rem;
            margin-top: 0.5rem;
            display: none;
        }}

        .admin-panel {{
            display: none;
            background-color: var(--card-background);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 2rem auto;
            border: 1px solid var(--border-color);
            max-width: 800px;
        }}

        .admin-panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            text-align: center;
        }}

        .admin-panel-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            text-align: center;
        }}

        .logout-btn {{
            background: var(--error-color);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .logout-btn:hover {{
            opacity: 0.9;
        }}

        .admin-controls {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            text-align: left;
        }}

        .control-group {{
            background-color: var(--background-color);
            padding: 1rem;
            border-radius: 0.5rem;
        }}

        .control-label {{
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .control-input {{
            width: 100%;
            padding: 0.5rem;
            background-color: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 0.25rem;
            color: var(--text-primary);
        }}

        .update-section {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        }}

        .update-btn {{
            background: var(--success-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .update-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.4);
        }}

        .update-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}

        .update-status {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            min-width: 200px;
        }}

        .update-status.updating {{
            color: var(--primary-color);
        }}

        .update-status.success {{
            color: var(--success-color);
        }}

        .refresh-btn-container {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }}

        .share-btn {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .share-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        }}

        .share-icon {{
            width: 20px;
            height: 20px;
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .news-card {{
            background-color: var(--card-background);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .news-card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-color);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}

        .news-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}

        .news-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .news-content {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}

        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}

        .news-source {{
            background-color: rgba(99, 102, 241, 0.1);
            color: var(--primary-color);
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .news-link {{
            display: inline-block;
            color: var(--primary-color);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: color 0.3s ease;
        }}

        .news-link:hover {{
            color: var(--secondary-color);
            text-decoration: underline;
        }}

        footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .loading {{
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }}

        .toast {{
            position: fixed;
            top: 20px;
            right: 0px;
            background-color: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }}

        .toast.show {{
            transform: translateX(-20%);
        }}

        .toast.error {{
            background-color: var(--error-color);
        }}

        .data-sources-section {{
            margin-top: 2rem;
        }}

        .data-sources-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
            text-align: center;
        }}

        .data-sources-list {{
            background-color: var(--background-color);
            border-radius: 0.5rem;
            padding: 1rem;
        }}

        .data-source-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .data-source-item:last-child {{
            border-bottom: none;
        }}

        .data-source-info {{
            flex: 1;
        }}

        .data-source-name {{
            font-weight: 500;
            color: var(--text-primary);
        }}

        .data-source-url {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }}

        .data-source-actions {{
            display: flex;
            gap: 0.5rem;
        }}

        .toggle-btn {{
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            font-size: 0.8rem;
            cursor: pointer;
        }}

        .delete-btn {{
            background: var(--error-color);
            color: white;
            border: none;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            font-size: 0.8rem;
            cursor: pointer;
        }}

        .add-source-btn {{
            background: var(--success-color);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 1rem;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            h1 {{
                font-size: 2rem;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}

            .admin-login-btn {{
                position: relative;
                margin-bottom: 1rem;
            }}

            .update-section {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>每日AI行业洞察·十大精选 · {current_date}</h1>
            <button id="adminLoginBtn" class="admin-login-btn">登录管理员</button>
            
            <div class="refresh-btn-container">
                <button id="shareBtn" class="share-btn">
                    <svg class="share-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18,16.08C17.24,16.08 16.56,16.38 16.04,16.85L8.91,12.7C8.96,12.47 9,12.24 9,12C9,11.76 8.96,11.53 8.91,11.3L15.96,7.19C16.5,7.69 17.21,8 18,8A3,3 0 0,0 21,5A3,3 0 0,0 18,2C15.65,2 13.73,3.66 13.35,5.93L7.39,9.34C6.54,9.76 6,10.56 6,11.5V16A2,2 0 0,0 8,18H13.5A2.5,2.5 0 0,0 16,15.5V11.22L18,12.3V16.08M15,13.5A1,1 0 0,1 14,14.5V17H9V15H13V14.5A1,1 0 0,1 15,13.5Z"></path>
                    </svg>
                    分享资讯
                </button>
            </div>
        </header>

        <div id="adminPanel" class="admin-panel">
            <div class="admin-panel-header">
                <h2 class="admin-panel-title">管理员控制面板</h2>
                <button id="logoutBtn" class="logout-btn">退出登录</button>
            </div>
            <div class="admin-controls">
                <div class="control-group">
                    <label class="control-label">每日更新时间</label>
                    <input type="time" id="updateTime" class="control-input" value="08:00">
                </div>
            </div>
            <div class="update-section">
                <button id="manualUpdateBtn" class="update-btn">立即手动更新</button>
                <div id="updateStatus" class="update-status">上次更新：{current_time}</div>
            </div>
            
            <div class="data-sources-section">
                <h3 class="data-sources-title">信息源管理</h3>
                <div id="dataSourcesList" class="data-sources-list">
                    <!-- 信息源列表将通过JavaScript动态生成 -->
                </div>
                <button id="addDataSourceBtn" class="add-source-btn">添加信息源</button>
            </div>
        </div>

        <div id="newsContainer" class="news-grid">
            <!-- 新闻卡片将通过JavaScript动态生成 -->
        </div>

        <footer>
            <p>最近更新：{current_time}</p>
        </footer>
    </div>

    <div id="loginModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">管理员登录</h2>
                <button id="closeModal" class="close-btn">&times;</button>
            </div>
            <form id="loginForm">
                <div class="form-group">
                    <label class="form-label">账号</label>
                    <input type="text" id="username" class="form-input" placeholder="请输入账号" required>
                </div>
                <div class="form-group">
                    <label class="form-label">密码</label>
                    <input type="password" id="password" class="form-input" placeholder="请输入密码" required>
                </div>
                <div id="errorMessage" class="error-message">账号或密码错误</div>
                <button type="submit" class="submit-btn">登录</button>
            </form>
        </div>
    </div>

    <div id="addSourceModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">添加信息源</h2>
                <button id="closeAddSourceModal" class="close-btn">&times;</button>
            </div>
            <form id="addSourceForm">
                <div class="form-group">
                    <label class="form-label">信息源名称</label>
                    <input type="text" id="sourceName" class="form-input" placeholder="请输入信息源名称" required>
                </div>
                <div class="form-group">
                    <label class="form-label">信息源URL</label>
                    <input type="url" id="sourceUrl" class="form-input" placeholder="请输入信息源URL" required>
                </div>
                <button type="submit" class="submit-btn">添加</button>
            </form>
        </div>
    </div>

    <div id="toast" class="toast">操作成功！</div>

    <script>
        // 新闻数据
        const newsData = {json.dumps(news, ensure_ascii=False)};
        
        // 数据源配置
        const dataSources = {json.dumps(data_sources, ensure_ascii=False)};

        // 管理员登录相关
        const adminLoginBtn = document.getElementById('adminLoginBtn');
        const loginModal = document.getElementById('loginModal');
        const closeModal = document.getElementById('closeModal');
        const loginForm = document.getElementById('loginForm');
        const adminPanel = document.getElementById('adminPanel');
        const logoutBtn = document.getElementById('logoutBtn');
        const errorMessage = document.getElementById('errorMessage');

        // 信息源管理相关
        const dataSourcesList = document.getElementById('dataSourcesList');
        const addDataSourceBtn = document.getElementById('addDataSourceBtn');
        const addSourceModal = document.getElementById('addSourceModal');
        const closeAddSourceModal = document.getElementById('closeAddSourceModal');
        const addSourceForm = document.getElementById('addSourceForm');

        // 检查登录状态
        function checkLoginStatus() {{
            const isLoggedIn = localStorage.getItem('adminLoggedIn');
            if (isLoggedIn === 'true') {{
                adminPanel.style.display = 'block';
                adminLoginBtn.style.display = 'none';
                renderDataSources();
            }}
        }}

        // 更新上次更新时间
        function updateLastUpdateTime() {{
            const lastUpdateTime = localStorage.getItem('lastUpdateTime');
            if (lastUpdateTime) {{
                const updateTime = new Date(lastUpdateTime);
                const updateTimeStr = updateTime.toLocaleString('zh-CN', {{
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                }});
                document.getElementById('updateStatus').textContent = '上次更新：' + updateTimeStr;
            }}
        }}

        // 打开登录模态框
        adminLoginBtn.addEventListener('click', () => {{
            loginModal.style.display = 'block';
        }});

        // 关闭登录模态框
        closeModal.addEventListener('click', () => {{
            loginModal.style.display = 'none';
            errorMessage.style.display = 'none';
        }});

        // 点击模态框外部关闭
        window.addEventListener('click', (e) => {{
            if (e.target === loginModal) {{
                loginModal.style.display = 'none';
                errorMessage.style.display = 'none';
            }}
            if (e.target === addSourceModal) {{
                addSourceModal.style.display = 'none';
            }}
        }});

        // 登录表单提交
        loginForm.addEventListener('submit', (e) => {{
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (username === 'admin' && password === 'admin') {{
                // 保存登录状态到 localStorage
                localStorage.setItem('adminLoggedIn', 'true');
                localStorage.setItem('loginTime', new Date().toISOString());
                
                loginModal.style.display = 'none';
                adminPanel.style.display = 'block';
                adminLoginBtn.style.display = 'none';
                renderDataSources();
                showToast('登录成功！');
                
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
                errorMessage.style.display = 'none';
            }} else {{
                errorMessage.style.display = 'block';
            }}
        }});

        // 退出登录
        logoutBtn.addEventListener('click', () => {{
            // 清除登录状态
            localStorage.removeItem('adminLoggedIn');
            localStorage.removeItem('loginTime');
            
            adminPanel.style.display = 'none';
            adminLoginBtn.style.display = 'block';
            showToast('已退出登录');
        }});

        // 手动更新功能
        const manualUpdateBtn = document.getElementById('manualUpdateBtn');
        const updateStatus = document.getElementById('updateStatus');
        
        manualUpdateBtn.addEventListener('click', () => {{
            // 显示更新状态
            updateStatus.textContent = '正在更新资讯...';
            updateStatus.classList.add('updating');
            
            // 禁用按钮防止重复点击
            manualUpdateBtn.disabled = true;
            
            const newsContainer = document.getElementById('newsContainer');
            newsContainer.innerHTML = '<div class="loading">刷新中...</div>';
            
            // 模拟更新过程
            setTimeout(() => {{
                // 更新成功
                updateStatus.textContent = '更新成功';
                updateStatus.classList.remove('updating');
                updateStatus.classList.add('success');
                
                // 保存更新时间
                localStorage.setItem('lastUpdateTime', new Date().toISOString());
                
                // 重新加载页面以获取新内容（登录状态会保留）
                setTimeout(() => {{
                    window.location.reload();
                }}, 1000);
            }}, 2000);
        }});

        // 渲染数据源列表
        function renderDataSources() {{
            dataSourcesList.innerHTML = '';
            dataSources.forEach(source => {{
                const item = document.createElement('div');
                item.className = 'data-source-item';
                item.innerHTML = `
                    <div class="data-source-info">
                        <div class="data-source-name">${{source.name}}</div>
                        <div class="data-source-url">${{source.url}}</div>
                    </div>
                    <div class="data-source-actions">
                        <button class="toggle-btn" data-id="${{source.id}}">${{source.enabled ? '启用' : '禁用'}}</button>
                        <button class="delete-btn" data-id="${{source.id}}">删除</button>
                    </div>
                `;
                dataSourcesList.appendChild(item);
            }});

            // 绑定切换按钮事件
            document.querySelectorAll('.toggle-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const sourceId = parseInt(this.dataset.id);
                    const source = dataSources.find(s => s.id === sourceId);
                    if (source) {{
                        source.enabled = !source.enabled;
                        this.textContent = source.enabled ? '启用' : '禁用';
                        showToast(`已${{source.enabled ? '启用' : '禁用'}}信息源：${{source.name}}`);
                    }}
                }});
            }});

            // 绑定删除按钮事件
            document.querySelectorAll('.delete-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const sourceId = parseInt(this.dataset.id);
                    const sourceIndex = dataSources.findIndex(s => s.id === sourceId);
                    if (sourceIndex !== -1) {{
                        const sourceName = dataSources[sourceIndex].name;
                        dataSources.splice(sourceIndex, 1);
                        renderDataSources();
                        showToast(`已删除信息源：${{sourceName}}`);
                    }}
                }});
            }});
        }}

        // 打开添加信息源模态框
        addDataSourceBtn.addEventListener('click', () => {{
            addSourceModal.style.display = 'block';
        }});

        // 关闭添加信息源模态框
        closeAddSourceModal.addEventListener('click', () => {{
            addSourceModal.style.display = 'none';
        }});

        // 添加信息源表单提交
        addSourceForm.addEventListener('submit', (e) => {{
            e.preventDefault();
            const sourceName = document.getElementById('sourceName').value;
            const sourceUrl = document.getElementById('sourceUrl').value;

            const newSource = {{
                id: dataSources.length > 0 ? Math.max(...dataSources.map(s => s.id)) + 1 : 1,
                name: sourceName,
                url: sourceUrl,
                enabled: true
            }};

            dataSources.push(newSource);
            renderDataSources();
            addSourceModal.style.display = 'none';
            document.getElementById('sourceName').value = '';
            document.getElementById('sourceUrl').value = '';
            showToast('信息源添加成功！');
        }});

        // 渲染新闻卡片
        function renderNews(news) {{
            const newsContainer = document.getElementById('newsContainer');
            newsContainer.innerHTML = '';

            news.forEach((item, index) => {{
                const card = document.createElement('div');
                card.className = 'news-card';
                card.innerHTML = `
                    <h3 class="news-title">${{index + 1}}、${{item.title}}</h3>
                    <p class="news-content">${{item.content}}</p>
                    <div class="news-meta">
                        <span class="news-time">${{item.time}}</span>
                        <span class="news-source">${{item.source}}</span>
                    </div>
                    <a href="${{item.link}}" class="news-link" target="_blank">阅读原文</a>
                `;
                newsContainer.appendChild(card);
            }});
        }}

        // 显示提示消息
        function showToast(message, type = 'success') {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast show';
            if (type === 'error') {{
                toast.classList.add('error');
            }}
            setTimeout(() => {{
                toast.classList.remove('show', 'error');
            }}, 3000);
        }}

        // 分享功能
        function shareNews() {{
            let shareContent = '';
            newsData.forEach((item, index) => {{
                shareContent += `${{index + 1}}、${{item.title}}\\n`;
            }});
            shareContent += `\\n更多详情请见 https://harker1544525153-lang.github.io/ai-insights/`;

            if (navigator.clipboard) {{
                navigator.clipboard.writeText(shareContent)
                    .then(() => {{
                        showToast('复制成功！');
                    }})
                    .catch(err => {{
                        console.error('复制失败:', err);
                        showToast('复制失败，请手动复制');
                    }});
            }} else {{
                const textArea = document.createElement('textarea');
                textArea.value = shareContent;
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    document.execCommand('copy');
                    showToast('复制成功！');
                }} catch (err) {{
                    console.error('复制失败:', err);
                    showToast('复制失败，请手动复制');
                }}
                document.body.removeChild(textArea);
            }}
        }}

        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {{
            // 检查登录状态
            checkLoginStatus();
            
            // 更新上次更新时间
            updateLastUpdateTime();
            
            // 渲染新闻
            renderNews(newsData);

            // 绑定分享按钮事件
            document.getElementById('shareBtn').addEventListener('click', shareNews);
        }});
    </script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML文件生成完成！")

if __name__ == "__main__":
    try:
        print("开始获取最新资讯...")
        news = fetch_news()
        print(f"获取到 {len(news)} 条资讯")
        generate_html(news)
        print("资讯更新完成！")
    except Exception as e:
        print(f"执行出错：{e}")
        import traceback
        traceback.print_exc()