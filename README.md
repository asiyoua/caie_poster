# bxz-poster-gen

> AI 课程/活动海报生成器 —— 基于 Gemini API 的本地海报生成工具

专为 AI 互联网和 AI 编程教育领域设计的垂直海报生成技能，固定品牌视觉风格，支持课程宣传、活动宣传等常见场景。

![Poster Type](https://img.shields.io/badge/type-education-blue)
![Gemini API](https://img.shields.io/badge/api-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)

---

## 特性

- **固定品牌风格** —— 3D C4D Octane 渲染 + Glassmorphism UI
- **垂直格式优化** —— 9:20 移动端优化比例
- **内置角色系统** —— Amy 老师 IP 形象
- **模块化布局** —— Header → 角色 → 内容 → CTA → Footer
- **批量生成** —— 支持一次生成多张不同风格的海报

---

## 快速开始

### 1. 安装依赖

```bash
pip install google-genai
```

### 2. 配置 API Key

创建配置文件并填入你的 Gemini API Key：

```bash
mkdir -p ~/.config/bxz-poster-gen
cat > ~/.config/bxz-poster-gen/config.ini << EOF
[gemini]
api_key = your-actual-api-key-here
model = gemini-3-pro-image-preview

[output]
default_dir = ~/Posters
default_format = png
EOF
```

### 3. 生成海报

```bash
python scripts/generate.py "AI产品经理实战营" \
  --subtitle "手把手教你做AI产品" \
  --content "12/22 开营分享" \
  --content "12/23 第一讲" \
  --content "12/25 第二讲" \
  --cta "限时特惠 299元"
```

---

## 海报类型

| 类型 | 用途 | 比例 |
|------|------|------|
| **Course** | 课程宣传、训练营招生 | 9:20 |
| **Event** | 线下活动、直播预告 | 9:16 |
| **Speaker** | 讲师介绍、个人品牌 | 9:20 |
| **Quote** | 金句分享、社交媒体 | 9:16 |

---

## 使用示例

### 课程宣传海报

```bash
python scripts/generate.py "AI产品经理实战营" \
  --subtitle "手把手教你做AI产品" \
  --content "12/22 开营分享" \
  --content "12/23 第一讲：敏捷验证" \
  --content "12/25 第二讲：效率革命" \
  --content "12/28 结营路演" \
  --cta "前100名 9.9元" \
  --output ~/Posters/course
```

### 活动宣传海报

```bash
python scripts/generate.py "AI产品分享会" \
  --subtitle "与行业专家面对面" \
  --content "12月28日 20:00" \
  --content "线上直播" \
  --cta "立即报名" \
  --aspect-ratio 9:16
```

### 金句海报

```bash
python scripts/generate.py "AI不会取代产品经理" \
  --subtitle "会用AI的产品经理会取代不会用的" \
  --aspect-ratio 9:16
```

---

## 品牌视觉规范

### 色彩系统

| 名称 | Hex值 | 用途 |
|------|-------|------|
| 深夜蓝 | `#0A192F` | 主背景色 |
| 荧光青 | `#00FFFF` | 强调色、高光 |
| 电光紫 | `#8B5CF6` | 次强调色 |
| 暖金黄 | `#FFD700` | CTA、价格高亮 |

### 渲染风格

- **风格**: 3D C4D Octane Rendering
- **材质**: 哑光乙烯基皮肤 + 注塑塑料装甲 + Glassmorphism
- **光照**: 戏剧性边缘光 + 多层次投影 + 次表面散射

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
  --subtitle SUBTITLE   副标题
  --content CONTENT     内容项（可多次使用）
  --cta CTA             CTA文本
  --footer FOOTER       页脚文字 (默认: CAIE人工智能研究院)
  --output OUTPUT       输出目录
  --api-key API_KEY     Gemini API Key
  --aspect-ratio        宽高比 (默认: 9:20)
```

---

## 输出结构

```
~/Posters/{topic-slug}/
├── poster-01.png        # 生成的海报
├── poster-01_prompt.txt # 使用的提示词
└── outline.md           # 生成说明
```

---

## 目录结构

```
bxz-poster-gen/
├── SKILL.md              # 技能定义文件
├── README.md             # 本文件
├── scripts/
│   ├── generate.py       # 核心生成脚本
│   └── templates.py      # 提示词模板
├── docs/
│   ├── USAGE.md          # 详细使用说明
│   └── 字节清晰度指南.md # 清晰度指南
└── config/
    └── config.ini        # 配置文件模板
```

---

## 在 Claude Code 中使用

### 直接调用

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

确保已正确配置 `~/.config/bxz-poster-gen/config.ini` 文件。

### 生成失败

- 检查 API Key 是否有效
- 检查网络连接
- 确认未超过 API 速率限制

### Git 推送问题

#### HTTP2 协议错误

**错误**: `fatal: unable to access 'https://github.com/...': Error in the HTTP2 framing layer`

**解决方案 1**: 使用 HTTP/1.1
```bash
git -c http.version=HTTP/1.1 push
```

**解决方案 2**: 使用带 Token 的 URL
```bash
git remote set-url origin https://<token>@github.com/username/repo.git
git push
```

**解决方案 3**: 配置全局 HTTP 版本
```bash
git config --global http.version HTTP/1.1
```

#### 连接超时

**错误**: `fatal: unable to access 'https://github.com/...': Couldn't connect to server`

**解决方案**: 检查网络或尝试使用 Token URL 方式（见上）

#### 凭据存储

macOS 用户可以使用钥匙串存储 GitHub Token：
```bash
git credential-osxkeychain store <<EOF
protocol=https
host=github.com
username=your-username
password=your-pat-token
EOF
```

---

## 致谢

本技能的设计参考了以下项目的最佳实践：

- [bxz-xhs](https://github.com/asiyoua/bxz-xhs) —— Style × Layout 矩阵架构
- [theme-factory](https://github.com/anthropics/anthropic-quickstarts) —— 色彩系统管理

---

## License

MIT
