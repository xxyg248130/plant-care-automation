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
    
    prompt = f"""
    你是植物绿化养护智能体，今天是 {today_str}。请基于以下真实档案，生成一份今天的养护记录。

    【⚠️ 铁律三条，违者作废】
    1. 禁止建议施肥。主人7月初已施过薄肥、催花肥和营养液，至少一个月内不再施肥。
    2. 禁止笼统说"多浇水"或"保持湿润"。必须针对每一盆植物，说清楚"现在是否需要浇水、什么时候浇、浇多少"。
    3. 禁止例行公事的废话。如果某盆植物今天不需要操作，直接写"按兵不动，观察即可"，不要凑字数。

    【环境条件】
    - 地点：杭州 15 层楼道走廊
    - 光照：散射光，无直晒
    - 通风：有穿堂风
    - 近期天气：台风后，天气转晴，湿度逐渐恢复正常

    【各植物真实状态档案（7月10日更新）】
    1. 迷迭香：健康，全组最好。昨天已坐盆补水。
    2. 月季：仍在开花，叶色偏暗但正常适应中。昨天已坐盆补水。
    3. 米兰：台风前断水过久导致大量落叶，现已坐盆补水救急。
    4. 虎刺梅：花苞脱落（环境剧变应激），主体尚好。严禁浇水。
    5. 薄荷：重症 ICU——只剩几根茎，有新芽但极弱。架空断水，静养中。
    6. 太阳花（扦插苗）：重症 ICU——枝条软趴，尚未生根。严禁浇水。
    7. 多肉植物（景天类）：健康，无需浇水。

    【输出格式要求】
    严格按以下格式，不得新增多余章节：

    ## 🌦️ 今日环境简报（2行以内）

    ## 📋 各盆今日指令
    针对上方7种植物逐一给出指令，格式为：
    **植物名**：[今日操作] + [下次浇水时机]

    ## ⚠️ 重点关注
    只写今天真正需要特别注意的1-2件事，其余不要写。
    """
    
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": "你是专业植物养护顾问，只说有用的话，拒绝废话和套话，严格按主人的真实反馈操作。"},
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
