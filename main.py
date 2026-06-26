import os
import datetime
from zhipuai import ZhipuAI

# 从环境变量获取 API Key
api_key = os.environ.get("ZHIPU_API_KEY")
if not api_key:
    raise ValueError("请设置 ZHIPU_API_KEY 环境变量！")

client = ZhipuAI(api_key=api_key)

def generate_record():
    today_str = datetime.datetime.now().strftime("%m月%d日")
    
    # 根据你 BILLY 里的真实数据量身定制的 Prompt
    prompt = f"""
    你是植物绿化养护智能体，今天是 {today_str}。
    请基于以下【植物档案】和【环境条件】，生成一份今天的养护记录和行动指令。

    【环境条件】
    - 地区：杭州
    - 位置：15层楼道走廊（非强日光，明亮的散射光，有自然风）
    - 季节：请根据当前日期（{today_str}）自动判断当前的气候特点（如是否梅雨季、是否高温等）

    【植物档案】
    1. 米兰（扦插苗，南方红壤）
    2. 月季（扦插苗，北方中壤黑土）
    3. 虎刺梅
    4. 太阳花、迷迭香、薄荷（春季播种，生长期）
    5. 国兰（室内窗台半阴通风处，使用专业兰石颗粒土，需防暴晒、防积水烂根，忌浓肥）

    【输出格式要求】
    请直接输出 Markdown 格式。包含以下几部分：
    ## 🌦️ 环境监控分析（结合杭州当前季节给出分析）
    ## 📋 今日行动指令（给出具体的浇水、施肥和病虫害排查建议）
    ## ⏭️ 明日待办与提醒
    """
    
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个专业的植物绿化养护专家，负责输出精准、实用的每日指令。"},
            {"role": "user", "content": prompt}
        ],
    )
    
    return response.choices[0].message.content

def main():
    print("正在呼叫智谱 GLM 大模型，思考今天的养护建议...")
    record_content = generate_record()
    
    # 确保输出目录存在
    if not os.path.exists("records"):
        os.makedirs("records")
        
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"records/{today}-养护记录.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {today} 植物养护自动记录\n\n")
        f.write(record_content)
        
    print(f"太棒了！成功生成记录文件: {filename}")

if __name__ == "__main__":
    main()
