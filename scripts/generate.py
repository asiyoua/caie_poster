#!/usr/bin/env python3
"""
bxz-poster-gen - 海报生成脚本
按场景生成优化过的 AI/编程/互联网类海报

场景说明：
1. 课程宣传 - 两张图拼接，科技风，文字+视觉并重
2. 活动宣传 - 单张图，可选风格（温暖/科技/简约），图片为主文字为辅
3. 产品宣传 - 单张图，冷色调科技风，需要产品截图，场景化+体验感
"""

import argparse
import configparser
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional, Dict

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("请先安装 google-genai: pip install google-genai")
    sys.exit(1)


# ============== 配置 ==============

DEFAULT_MODEL = "gemini-3-pro-image-preview"
REQUEST_DELAY = 2

# API Key 配置路径
API_KEY_CONFIGS = [
    "~/.config/bxz-poster-gen/config.ini",
    "~/.config/bxz-xhs/config.ini",
]

# 活动宣传风格选项
EVENT_STYLES = {
    "warm": "温暖治愈风",
    "tech": "赛博科技风",
    "minimal": "极简现代风"
}


# ============== 工具函数 ==============

def get_api_key() -> Optional[str]:
    """从配置文件获取 API Key"""
    for config_path in API_KEY_CONFIGS:
        config_path = Path(config_path).expanduser()
        if config_path.exists():
            try:
                config = configparser.ConfigParser()
                config.read(config_path)
                for section in ['gemini', 'gemini_nano', 'google']:
                    if section in config:
                        for key in ['api_key', 'apikey', 'key']:
                            if key in config[section]:
                                api_key = config[section][key].strip()
                                if api_key and api_key != 'your-api-key-here':
                                    return api_key
            except Exception:
                continue
    return None


def create_client(api_key: str) -> genai.Client:
    """创建 Google GenAI 客户端"""
    return genai.Client(api_key=api_key)


def generate_image(client: genai.Client, prompt: str, aspect_ratio: str) -> Optional[bytes]:
    """使用 Gemini API 生成图片"""
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio
                )
            )
        )

        for part in response.parts:
            if part.inline_data is not None:
                return part.inline_data.data

        print("  响应中没有图片数据")
        return None

    except Exception as e:
        print(f"  生成失败: {e}")
        return None


def sanitize_filename(name: str) -> str:
    """清理文件名"""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:100] if len(name) > 100 else name


def slugify(text: str) -> str:
    """将文本转换为 URL 友好的 slug"""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:50]


def encode_image_to_base64(image_path: str) -> str:
    """将图片编码为 base64"""
    import base64
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


# ============== 提示词构建函数 ==============

def build_course_prompts(info: Dict) -> list:
    """课程宣传海报提示词 - 完整版，分两张图拼接

    图1用 9:12，图2用 9:8，拼接后约 9:20
    """

    title = info['title']
    subtitle = info['subtitle']
    stats1 = info.get('stats1', '1期200+人报名')
    stats2 = info.get('stats2', '好评率高达96.8%')
    benefits = info.get('benefits', [])  # 口语化核心卖点
    schedule = info.get('schedule', [])
    audiences = info.get('audiences', ['想转行的产品经理/运营人员', '创业者/自由职业者', '有AI产品基础想进阶的产品经理'])
    cta = info.get('cta', '扫码锁定席位')

    # 图1：上半部分 (9:12) - Header + Hero + 信任背书 + 核心卖点
    prompt1 = f"""帮我画张课程海报宣传图的上半部分：'''
【最高优先级要求】所有文字必须超大、超清晰、毫不含糊！文字清晰度优先于所有视觉效果！

整体风格与构图定义
高质量 C4D Octane 渲染的 3D 赛博朋克风格。
材质上追求顶级潮玩手办的触感，结合了细腻的哑光乙烯基皮肤、带有微磨损的注塑塑料装甲，以及高反光的玻璃面罩，完美融合赛博朋克科技感。
主色调为深邃的午夜蓝底色，搭配高亮的霓虹青色、电光紫色和暖橙色光效。
大量使用具有真实厚度和光线折射的磨砂玻璃拟态 UI 面板、多层级的发光全息投影和在体积雾中漂浮的科技粒子。
整体光影富有史诗级电影感，强调戏剧性的边缘光勾勒角色轮廓，主光源在材质上产生真实的次表面散射效果，极大地增强体积感和高级感。

版式结构与内容填充（上半部分）

1. 顶部 Header 区域：
最上方是一个发光的胶囊形标题栏，文字为蓝光霓虹效果："{title}"。
紧接着是视觉中心的主标题，采用巨大、醒目的3D立体发光、有质感的字体："{subtitle}"。

2. 核心视觉 Hero 区域：
主角（叙事与质感升级）：
主标题下方，一个设计独特、充满探索欲的 3D 科技潮玩女性角色。
仅展露上半身，穿着带有微小机械细节未来服饰、戴着高科技透明AR 眼镜、发型很潮。

叙事性动作：
角色并非静止操作，而是面向左侧，身体前倾，正伸出手指向面前复杂的全息数据界面进行交互，脸上带着发现新大陆般的惊喜与开心表情，仿佛刚刚解锁了核心科技。

环境互动：
界面中漂浮的数据流环绕在角色周围，光芒照亮了角色的脸部，形成真实的色彩溢出。
背景不再是单纯平面，而是具有深度的赛博空间，隐约可见的数据塔和光缆在体积雾中若隐若现，营造极强的沉浸感。

3. 信任背书（关键点优化融合）：
在主角的头部左侧，因点击全息界面后，悬浮着一个醒目的金色/暖橙色全息数据徽章。
融合感：
徽章是从主界面中延伸投影出的全息荣誉勋章，带有微妙的数字噪点和光线抖动效果。
上面清晰地展示着两行超大超粗高亮数据，每个字都清晰可读："{stats1}" 和 "{stats2}"，
旁边带有一个具有立体浮雕感和内部发光的 3D 点赞（Thumbs up）图标，强调课程的火爆与口碑。

4. 核心卖点区（磨砂玻璃结构）：
容器外观：
宽大的圆角矩形磨砂玻璃面板，边缘带有青色微光，背景有淡淡的网格纹理。
顶部标签：
顶部是醒目的横向通透胶囊标签："你能收获"。

核心内容（所有文字必须超大超粗超清晰！！！）：
竖直排列的卖点列表：
"""

    for i, benefit in enumerate(benefits, 1):
        prompt1 += f"{i}. {benefit}\n"

    prompt1 += """注意：保持原有设计感，文字清晰可读即可！上下留出拼接空间！
'''"""

    # 图2：下半部分 (9:8) - 课程安排 + 适合人群 + 价值卡片 + 二维码区
    prompt2 = f"""帮我画张课程海报宣传图的下半部分：'''
【最高优先级要求】所有文字必须超大、超清晰、毫不含糊！文字清晰度优先于所有视觉效果！

整体风格与上图保持一致！高质量 C4D Octane 渲染的 3D 赛博朋克风格。
主色调为深邃的午夜蓝底色，搭配高亮的霓虹青色、电光紫色和暖橙色光效。
大量使用具有真实厚度和光线折射的磨砂玻璃拟态 UI 面板。

版式结构与内容填充（下半部分）

1. 核心信息区（磨砂玻璃结构）：
容器外观：
宽大的圆角矩形磨砂玻璃面板，边缘带有青色微光，背景有淡淡的网格纹理。
顶部标签：
顶部是醒目的横向通透胶囊标签："课程安排"。

核心内容（此模块是海报核心信息，所有文字必须超大超粗超清晰！！！）：
竖直排列的时间轴列表：
"""

    for item in schedule:
        prompt2 += f"{item}\n"

    prompt2 += """右侧装饰（关键视觉点）：
在面板的右下角，站着一组（3个）迷你的 Q 版 3D 可爱角色。
动作细节：
它们紧紧挤在一起，表情兴奋，有的拿着笔，有的指着上面的课程表，
仿佛在热烈讨论学习计划，为画面增添生动的故事感。

2. 适合人群区：
容器外观：
一个低调的、扁平的条状磨砂玻璃面板。
高度很窄，边缘带有青色微光，背景有淡淡的网格纹理。
顶部标签：
顶部是醒目的横向通透胶囊标签："适合人群"。

核心布局（横向排列，所有文字必须超大超粗超清晰可读！！！）：
面板中央水平排列着三组信息单元，展示浮动元素与文字。
"""

    audience_icons = ['戴眼镜 3D 男性头像', '充满活力的 3D 中国女性头像', '好奇宝宝 3D 学生头像']
    positions = ['左单元', '中单元', '右单元']

    for i, (aud, icon) in enumerate(zip(audiences, audience_icons)):
        prompt2 += f"{positions[i]}： 上方悬浮一个{icon}（伴随微小装饰）；紧接着下方是超大超粗清晰文字：\"{aud}\"。\n"

    prompt2 += """3. 课程价值卡片区（四个并排、扁平）：
四个并排的圆角磨砂玻璃卡片，每张卡片标题左侧有不同颜色的发光3D 图标。
请根据上面课程安排的内容，为每个卡片自动生成一个相关的标题和图标（火箭/齿轮/芯片/奖杯/闪电/钻石等），确保标题与课程内容匹配！
"""

    for i in range(min(4, len(schedule))):
        if ' - ' in schedule[i]:
            desc = schedule[i].split(' - ')[1][:30]
        else:
            desc = schedule[i][:30]
        prompt2 += f"[卡片{i+1}]：根据课程内容\"{desc}\"自动生成合适的标题、图标和描述。\n"

    prompt2 += f"""4. 底部二维码区（空间大、很高）：
顶部的横幅标题栏为一个蓝金双色交织的电光标题栏，
文字"{cta}"以超大超粗高亮发光字体呈现，每个字都清晰可读。
下方是一个很高的、占据底部大部分空间的方形发光二维码区域，
其周围环绕着强烈的蓝色和金色圆形闪电能量场。
电光纹理向外放射，仿佛要冲破屏幕，
二维码本身被一个复杂的能量框包裹，内部有电流涌动。
一个 3D 可爱角色在旁边兴奋地指向这个巨大的电光二维码区域，
其指尖和身体被蓝金色的电光照亮，做出强烈推荐的手势。

5. 页脚 Footer：
海报最底部边缘，小字显示："CAIE人工智能研究院"。

注意：保持与上图风格一致，所有文字清晰可读！
'''"""

    return [prompt1, prompt2]


def build_event_prompt(info: Dict, style: str) -> str:
    """活动宣传海报提示词 - 单张图

    style: warm/tech/minimal
    视觉效果突出，文字为辅
    """

    title = info['title']
    subtitle = info['subtitle']
    benefits = info.get('benefits', [])
    cta = info['cta']

    if style == "warm":
        style_desc = """整体风格：温暖治愈系插画风格，柔和舒适。
材质：水彩纸纹理 + 柔和渐变 + 毛绒质感元素。
主色调：奶油米色底色 (#FFF8E7)，搭配蜜桃粉 (#FFB6B9)、薄荷绿 (#98D8C8)、暖黄色 (#FFE066)。
特效：柔和的光斑、飘落的花瓣/羽毛、温暖的发光圆环。
光影：柔和自然光，像午后的阳光透过窗户洒进来。"""
        role_desc = """温柔亲和的女性角色（亚洲），穿着舒适毛衣，温暖微笑。
背景有柔和的光斑、飘落的樱花花瓣。"""
        card_desc = "宽大的圆角卡片，柔和渐变背景，边缘有温暖发光圆环。"
    elif style == "tech":
        style_desc = """整体风格：赛博朋克科技风格，未来感十足。
材质：磨砂玻璃 + 霓虹光效 + 金属质感边框。
主色调：深空蓝底色 (#0A1929)，搭配霓虹青 (#00E5FF)、电光紫 (#AA00FF)。
特效：全息投影、数据流、能量场、粒子效果。
光影：戏剧性边缘光，霓虹发光效果。"""
        role_desc = """充满科技感的虚拟角色，半透明数字身体，数据流环绕。
背景是赛博空间，漂浮的全息界面。"""
        card_desc = "发光的玻璃态面板，边缘有霓虹光效，背景有网格纹理。"
    else:  # minimal
        style_desc = """整体风格：极简现代设计风格，干净利落。
材质：纯色平面 + 细线条 + 几何图形。
主色调：纯白底色 (#FFFFFF)，搭配黑色 (#000000)、单色强调色。
特效：简洁的几何装饰、细线条分隔、大量留白。
光影：平面化设计，最小阴影。"""
        role_desc = """简约的几何图形组合，抽象的人物轮廓。
背景干净，大量留白。"""
        card_desc = "简洁的扁平卡片，细边框，纯色背景。"

    prompt = f"""帮我画一张活动宣传海报：'''
【最高优先级要求】所有文字必须超大、超清晰、毫不含糊！文字清晰度优先于所有视觉效果！
{style_desc}

版式结构：
1. 顶部标题区：
超大醒目标题：\"{title}\"
副标题（超大清晰）：\"{subtitle}\"

2. 核心视觉区：
{role_desc}

3. 核心福利区：
{card_desc}
内含福利列表：
"""

    for i, benefit in enumerate(benefits, 1):
        prompt += f"{i}. {benefit}\n"

    prompt += f"""4. 中央大二维码区：
超大二维码区域，周围有装饰性光效。
二维码下方有清晰文字（超大超粗）："扫码立即参与"。

5. 底部 CTA 区：
醒目的横幅。
超大超粗高亮文字：\"{cta}\"

注意：视觉效果突出，文字简洁！留出二维码位置！
'''"""

    return prompt


def build_product_prompt(info: Dict) -> str:
    """产品宣传海报提示词 - 单张图

    冷色调科技风
    场景化 + 体验感
    """

    title = info['title']
    subtitle = info.get('subtitle', '')
    features = info.get('features', [])  # 场景化功能点
    value = info.get('value', '')
    cta = info.get('cta', '立即体验')
    product_image = info.get('product_image', '')

    # 如果有产品截图，在提示词中引用
    image_ref = f"""
【产品参考】
请参考这张产品的界面截图，在海报中展示产品界面：
{product_image}
""" if product_image else ""

    prompt = f"""帮我画一张产品宣传海报：'''
【最高优先级要求】所有文字必须超大、超清晰、毫不含糊！文字清晰度优先于所有视觉效果！

整体风格：互联网科技感，冷色调，简洁大气。
材质：磨砂玻璃面板 + 金属边框 + 渐变背景。
主色调：深灰蓝底色 (#1E293B)，搭配冰蓝色 (#38BDF8)、银灰色 (#94A3B8)。
特效：数据流、连接节点、发光线条、科技粒子。
光影：柔和冷光，边缘发光效果。
{image_ref}
版式结构（从上到下）：
1. 顶部产品名区：
超大超粗醒目标题：\"{title}\""""

    if subtitle:
        prompt += f"""
产品slogan：\"{subtitle}\""""

    prompt += f"""

2. 核心功能区（场景化展示）：
展示产品在实际使用场景中的体验：
"""

    for i, feature in enumerate(features, 1):
        prompt += f"{i}. {feature}\n"

    if value:
        prompt += f"""
3. 价值主张区：
简短有力的价值陈述（超大超粗）：\"{value}\""""

    prompt += f"""
4. 底部 CTA 区：
超大超粗文字：\"{cta}\"
中央大二维码区域，周围有科技感装饰。

注意：冷色调科技风，场景化展示用户体验，文字简洁！
'''"""

    return prompt


# ============== 交互式信息收集 ==============

def collect_course_info() -> Dict:
    """收集课程宣传信息"""
    info = {}
    print("\n📚 课程宣传海报")
    print("-" * 50)

    info['title'] = input("课程标题（如：AI项目实战营）: ").strip()
    info['subtitle'] = input("副标题/Slogan（如：转型AI产品经理必看的Agent实战课）: ").strip()

    print("\n📊 信任背书数据（可选）:")
    info['stats1'] = input("数据1 (默认: 1期200+人报名): ").strip() or "1期200+人报名"
    info['stats2'] = input("数据2 (默认: 好评率高达96.8%): ").strip() or "好评率高达96.8%"

    print("\n💎 核心卖点（3-4条，口语化表达，如\"你可以收获...\"）:")
    benefits = []
    while len(benefits) < 4:
        benefit = input(f"卖点{len(benefits)+1} (直接回车结束): ").strip()
        if not benefit:
            break
        benefits.append(benefit)
    if not benefits:
        benefits = ["你可以收获一套完整的AI产品方法论", "你可以带走自己创作的实战作品", "你可以掌握Claude Code等顶级工具"]
    info['benefits'] = benefits

    print("\n📅 课程安排（4条左右）:")
    schedule = []
    while len(schedule) < 6:
        item = input(f"安排{len(schedule)+1} (直接回车结束): ").strip()
        if not item:
            break
        schedule.append(item)
    if not schedule:
        schedule = [
            "12/22（周一) 20:00  开营分享 - 经验拆解",
            "12/23（周二）20:00 第一讲 - 极速上手",
            "12/25（周四）20:00 第二讲 - 硬核实战",
            "12/28（周日）20:00 结营路演 - 学员作品show"
        ]
    info['schedule'] = schedule

    print("\n👥 适合人群（3组）:")
    print("1. 想转行的产品经理/运营人员")
    print("2. 创业者/自由职业者")
    print("3. 有AI产品基础想进阶的产品经理")
    use_default = input("使用默认? (y/n, 默认y): ").strip().lower()
    if use_default == 'n':
        audiences = []
        while len(audiences) < 3:
            aud = input(f"人群{len(audiences)+1}: ").strip()
            if aud:
                audiences.append(aud)
        info['audiences'] = audiences
    else:
        info['audiences'] = ['想转行的产品经理/运营人员', '创业者/自由职业者', '有AI产品基础想进阶的产品经理']

    info['cta'] = input("底部CTA (默认: 扫码锁定席位): ").strip() or "扫码锁定席位"
    return info


def collect_event_info() -> Dict:
    """收集活动宣传信息"""
    info = {}
    print("\n🎉 活动宣传海报")
    print("-" * 50)

    # 选择风格
    print("\n🎨 请选择视觉风格：")
    for key, name in EVENT_STYLES.items():
        print(f"  {key}. {name}")
    style_choice = input("选择 (默认: warm): ").strip().lower()
    if style_choice not in EVENT_STYLES:
        style_choice = "warm"
    info['style'] = style_choice
    print(f"已选择：{EVENT_STYLES[style_choice]}")

    info['title'] = input("\n活动标题: ").strip()
    info['subtitle'] = input("副标题: ").strip()

    print("\n🎁 核心福利亮点（3条左右，视觉展示为主）:")
    benefits = []
    while len(benefits) < 3:
        benefit = input(f"福利{len(benefits)+1} (直接回车结束): ").strip()
        if not benefit:
            break
        benefits.append(benefit)
    if not benefits:
        benefits = ["限时特惠，立省50%", "前100名送独家资料包", "推荐好友双方各得奖励"]
    info['benefits'] = benefits

    info['cta'] = input("\n底部CTA (如: 限时福利 立即参与): ").strip() or "限时福利 立即参与"
    return info


def collect_product_info() -> Dict:
    """收集产品宣传信息"""
    info = {}
    print("\n🚀 产品宣传海报")
    print("-" * 50)

    info['title'] = input("产品名称: ").strip()
    info['subtitle'] = input("Slogan（可选，按回车跳过）: ").strip()

    # 产品截图路径
    image_path = input("\n产品界面截图路径（可选，按回车跳过）: ").strip()
    if image_path and Path(image_path).expanduser().exists():
        info['product_image'] = encode_image_to_base64(Path(image_path).expanduser())
        print("  产品截图已加载")
    else:
        info['product_image'] = ""
        print("  无产品截图，将使用通用设计")

    print("\n⚡ 核心功能（3-4个，场景化描述用户体验）:")
    print("提示：用场景化方式描述，如\"一键生成，快速验证想法\"")
    features = []
    while len(features) < 4:
        feature = input(f"功能{len(features)+1}: ").strip()
        if not feature:
            break
        features.append(feature)
    if not features:
        features = ["一键生成，快速验证想法", "智能协作，提升团队效率", "实时预览，所见即所得"]
    info['features'] = features

    info['value'] = input("\n价值主张（可选）: ").strip() or "让技术更简单，让创新更快速"
    info['cta'] = input("底部CTA (默认: 立即体验): ").strip() or "立即体验"
    return info


# ============== 生成函数 ==============

def generate_single_poster(prompt: str, output_path: Path, filename: str, api_key: str, aspect_ratio: str) -> bool:
    """生成单张海报"""
    client = create_client(api_key)

    print(f"⏳ 正在调用 Gemini API (比例: {aspect_ratio})...")
    image_data = generate_image(client, prompt, aspect_ratio)

    if image_data:
        output_file = output_path / f"{filename}.png"
        output_file.write_bytes(image_data)

        # 保存提示词
        prompt_file = output_path / f"{filename}_prompt.txt"
        prompt_file.write_text(prompt, encoding='utf-8')

        print(f"✅ 保存成功: {output_file}")
        return True
    else:
        print(f"❌ 生成失败")
        return False


def generate_poster(scene: str, info: Dict, output_dir: str = None, api_key: str = None) -> dict:
    """根据场景生成海报"""

    if not api_key:
        api_key = get_api_key()
        if not api_key:
            print("❌ 无法找到 API Key")
            return {"success": False}

    # 设置输出目录
    if output_dir:
        output_path = Path(output_dir).expanduser()
    else:
        topic_slug = slugify(info['title'])
        output_path = Path.home() / "Posters" / scene / topic_slug
    output_path.mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(info['title'])

    # 保存信息
    info_file = output_path / f"{filename}_info.json"
    info_file.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')

    # 课程宣传：两张图拼接（使用支持的宽高比 9:16 + 9:16）
    if scene == "course":
        prompts = build_course_prompts(info)
        output_files = []

        # 图1: 9:16 (上半部分)
        if generate_single_poster(prompts[0], output_path, f"{filename}_part1", api_key, "9:16"):
            output_files.append(str(output_path / f"{filename}_part1.png"))
        else:
            return {"success": False}

        time.sleep(REQUEST_DELAY)

        # 图2: 9:16 (下半部分)
        if generate_single_poster(prompts[1], output_path, f"{filename}_part2", api_key, "9:16"):
            output_files.append(str(output_path / f"{filename}_part2.png"))
        else:
            return {"success": False}

        # 自动拼接
        print("🔄 正在拼接图片...")
        from PIL import Image
        img1 = Image.open(output_files[0])
        img2 = Image.open(output_files[1])
        width = img1.width
        total_height = img1.height + img2.height
        merged = Image.new('RGB', (width, total_height))
        merged.paste(img1, (0, 0))
        merged.paste(img2, (0, img1.height))
        merged_file = output_path / f"{filename}_完整.png"
        merged.save(merged_file)
        print(f"✅ 拼接完成: {merged_file}")

        # 删除分图（用户只看拼接后的图）
        Path(output_files[0]).unlink()
        Path(output_files[1]).unlink()
        # 同时删除对应的提示词文件
        Path(output_path / f"{filename}_part1_prompt.txt").unlink()
        Path(output_path / f"{filename}_part2_prompt.txt").unlink()
        print("🗑️  已删除分图，保留拼接后的完整图")

        return {
            "success": True,
            "output_file": str(merged_file),
            "message": "✅ 课程海报已生成并拼接"
        }

    # 活动宣传：单张图，风格可选
    elif scene == "event":
        style = info.get('style', 'warm')
        prompt = build_event_prompt(info, style)

        if generate_single_poster(prompt, output_path, filename, api_key, "9:16"):
            return {
                "success": True,
                "output_file": str(output_path / f"{filename}.png"),
                "message": f"✅ 活动海报已生成 ({EVENT_STYLES[style]})"
            }
        return {"success": False}

    # 产品宣传：单张图，冷色调科技风
    elif scene == "product":
        prompt = build_product_prompt(info)

        if generate_single_poster(prompt, output_path, filename, api_key, "9:16"):
            return {
                "success": True,
                "output_file": str(output_path / f"{filename}.png"),
                "message": "✅ 产品海报已生成"
            }
        return {"success": False}


# ============== 命令行接口 ==============

def main():
    parser = argparse.ArgumentParser(
        description="bxz-poster-gen - AI/编程/互联网类海报生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  课程宣传（两张图拼接）:
    python generate.py --scene course

  活动宣传（单张图，可选风格）:
    python generate.py --scene event

  产品宣传（单张图，冷色调科技风）:
    python generate.py --scene product
        """
    )

    parser.add_argument("--scene", "-s", required=True,
                        choices=["course", "event", "product"],
                        help="海报场景类型")
    parser.add_argument("--output", "-o", help="输出目录")
    parser.add_argument("--api-key", help="Gemini API Key")
    parser.add_argument("--info", "-i", help="从JSON文件读取信息（跳过交互式输入）")

    args = parser.parse_args()

    # 场景说明
    scene_desc = {
        "course": "课程宣传（两张图拼接，科技风）",
        "event": "活动宣传（单张图，可选风格）",
        "product": "产品宣传（单张图，冷色调科技风）"
    }

    print(f"\n{'='*50}")
    print(f"🎨 {scene_desc[args.scene]}")
    print(f"{'='*50}")

    # 交互式收集信息
    collect_funcs = {
        "course": collect_course_info,
        "event": collect_event_info,
        "product": collect_product_info
    }

    # 如果指定了 --info 参数，从 JSON 文件读取
    if args.info:
        with open(args.info, 'r', encoding='utf-8') as f:
            info = json.load(f)
        print(f"\n从文件读取: {args.info}")
    else:
        info = collect_funcs[args.scene]()

    if not info:
        sys.exit(1)

    # 确认
    print("\n" + "="*50)
    print("📝 信息确认")
    print("="*50)
    for k, v in info.items():
        if k == 'product_image' and v:
            print(f"{k}: [产品截图已加载]")
        elif isinstance(v, list):
            print(f"{k}: {len(v)} 项")
            for i in v:
                print(f"  - {i}")
        else:
            print(f"{k}: {v}")
    print("="*50)

    # 如果是 --info 模式，自动确认
    if args.info:
        confirm = 'y'
    else:
        confirm = input("\n确认生成? (y/n, 默认y): ").strip().lower()
    if confirm == 'n':
        print("已取消")
        sys.exit(1)

    result = generate_poster(
        scene=args.scene,
        info=info,
        output_dir=args.output,
        api_key=args.api_key
    )

    if result.get("success"):
        print(f"\n{result.get('message', '生成成功')}")
        print(f"📁 输出文件: {result.get('output_file')}")
        sys.exit(0)
    else:
        print("\n生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
