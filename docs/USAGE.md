# bxz-poster-gen 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install google-genai
```

### 2. 配置 API Key

创建配置文件：
```bash
mkdir -p ~/.config/bxz-poster-gen
cp /Users/bian/.claude/skills/bxz-poster-gen/config/config.ini ~/.config/bxz-poster-gen/config.ini
```

编辑 `~/.config/bxz-poster-gen/config.ini`，填入你的 Gemini API Key：
```ini
[gemini]
api_key = your-actual-api-key-here
```

### 3. 生成海报

```bash
python /Users/bian/.claude/skills/bxz-poster-gen/scripts/generate.py "AI产品经理实战营"
```

---

## 命令行参数

```
usage: generate.py [-h] [--subtitle SUBTITLE] [--content CONTENT] [--cta CTA]
                   [--footer FOOTER] [--output OUTPUT] [--api-key API_KEY]
                   [--aspect-ratio {1:1,16:9,9:16,4:3,3:4,9:20}]
                   title

positional arguments:
  title                 海报标题

optional arguments:
  -h, --help            显示帮助信息
  --subtitle SUBTITLE, -s SUBTITLE
                        副标题
  --content CONTENT, -c CONTENT
                        内容项（可多次使用）
  --cta CTA             CTA文本
  --footer FOOTER, -f FOOTER
                        页脚文字 (默认: CAIE人工智能研究院)
  --output OUTPUT, -o OUTPUT
                        输出目录
  --api-key API_KEY     Gemini API Key
  --aspect-ratio {1:1,16:9,9:16,4:3,3:4,9:20}, -r {1:1,16:9,9:16,4:3,3:4,9:20}
                        宽高比 (默认: 9:20)
```

---

## 使用示例

### 课程宣传海报

```bash
python generate.py "AI产品经理实战营" \
  --subtitle "手把手教你做AI产品" \
  --content "12/22 开营分享" \
  --content "12/23 第一讲：敏捷验证" \
  --content "12/25 第二讲：效率革命" \
  --content "12/28 结营路演" \
  --cta "🌟限时特惠，原价299元，前100名9.9元" \
  --output ~/Posters/ai-product-course
```

### 活动宣传海报

```bash
python generate.py "AI产品分享会" \
  --subtitle "与行业专家面对面" \
  --content "时间：12月28日 20:00" \
  --content "地点：线上直播" \
  --content "嘉宾：Amy老师" \
  --cta "立即报名" \
  --aspect-ratio 9:16
```

### 金句海报

```bash
python generate.py "AI不会取代产品经理" \
  --subtitle "会用AI的产品经理会取代不会用的" \
  --aspect-ratio 9:16
```

---

## Python API 使用

### 快速生成课程海报

```python
from poster_gen.scripts.generate import generate_course_poster

result = generate_course_poster(
    course_name="AI产品经理实战营",
    course_schedule=[
        "12/22 开营分享",
        "12/23 第一讲：敏捷验证",
        "12/25 第二讲：效率革命",
        "12/28 结营路演"
    ],
    price_info="🌟限时特惠，原价299元，前100名9.9元",
    api_key="your-api-key"
)
```

### 自定义海报

```python
from poster_gen.scripts.generate import generate_poster

result = generate_poster(
    title="AI产品分享会",
    subtitle="与行业专家面对面",
    content_items=[
        "时间：12月28日 20:00",
        "地点：线上直播",
        "嘉宾：Amy老师"
    ],
    cta_text="立即报名",
    footer="CAIE人工智能研究院",
    output_dir="~/Posters/event",
    api_key="your-api-key",
    aspect_ratio="9:16"
)
```

---

## 输出文件结构

生成的文件保存在 `~/Posters/{topic-slug}/` 目录：

```
~/Posters/ai-product-manager/
├── AI产品经理实战营.png          # 生成的海报图片
├── AI产品经理实战营_prompt.txt    # 使用的提示词
└── outline.md                     # 生成说明（如有）
```

---

## 在 Claude Code 中使用

### 直接调用

在 Claude Code 中直接说：

```
请生成一张课程宣传海报，主题是"AI产品经理实战营"
```

### 使用 Skill

```
/bxz-poster-gen AI产品经理实战营 --subtitle "手把手教你做AI产品"
```

---

## 故障排除

### API Key 错误

```
❌ 请提供 API Key (--api-key) 或配置 ~/.config/bxz-poster-gen/config.ini
```

**解决方法**: 确保已正确配置 API Key

### 生成失败

```
⚠️ 生成失败: ...
```

**可能原因**:
1. API Key 无效
2. 网络连接问题
3. API 速率限制
4. 提示词内容违规

**解决方法**:
- 检查 API Key 是否有效
- 等待几秒后重试
- 检查提示词内容

### 输出目录权限问题

**解决方法**:
```bash
mkdir -p ~/Posters
chmod 755 ~/Posters
```
