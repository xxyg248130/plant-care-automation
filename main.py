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
    请基于以下【植物档案】、【主人最新实况反馈】和【环境条件】，生成一份今天的养护记录和行动指令。
    
    【⚠️ 核心死命令：拒绝套话与乱施肥】
    1. 主人已经明确表示：上周已经全部施过薄肥和催花肥（月季、太阳花等），绿叶营养液也用过了。**禁止在任何情况下再建议施肥！**
    2. 绝不允许使用“夏季高温植物喜水，请多浇水”这种百科套话。现在是高湿黄梅天，宁干勿湿！如果不清楚状况，宁可建议“按兵不动，拍照询问”。

    【环境条件】
    - 地区：杭州
    - 位置：15层楼道走廊（非强日光，明亮的散射光，有自然风，近期极度高湿）

    【主人最新实况反馈（当前植物状态）】
    1. 迷迭香：最省心，稍微浇一点点水就活得很好。
    2. 太阳花和薄荷：重症 ICU 抢救中，处于被摧残得不成样子的虚弱期，严禁浇水施肥。
    3. 月季和米兰：处于环境适应期，状态比刚买来差一点，属正常退绿落花，需控水。
    4. 虎刺梅：出现非老化性黄叶，一抖就掉（疑为高湿/环境剧变应激反应），必须严格断水。

    【输出格式要求】
    请直接输出 Markdown 格式。包含以下几部分：
    ## 🌦️ 环境监控分析（结合杭州当前季节及走廊高湿环境）
    ## 📋 今日行动指令（基于主人的真实反馈，给出具体建议，绝不准乱提施肥）
    ## ⏭️ 明日待办与提醒
    """
    
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": "你是一个专业的植物绿化养护专家，必须严格听从主人的实际反馈，拒绝废话和套话。"},
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
