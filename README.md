# bxz-poster-gen

> AI 课程/活动海报生成器 —— 基于 Gemini API 的本地海报生成工具

专为 AI 互联网和 AI 编程教育领域设计的垂直海报生成技能，固定品牌视觉风格。

## 功能特性

- **固定品牌风格** —— 3D C4D Octane 渲染 + Glassmorphism UI
- **垂直格式优化** —— 9:20 移动端优化比例
- **内置角色系统** —— Amy 老师 IP 形象
- **模块化布局** —— Header → 角色 → 内容 → CTA → Footer
- **批量生成** —— 支持一次生成多张不同风格的海报

## 安装

```bash
pip install google-genai
```

## 配置

创建配置文件：

```bash
mkdir -p ~/.config/bxz-poster-gen
cat > ~/.config/bxz-poster-gen/config.ini << EOF
[gemini]
api_key = your-gemini-api-key
model = gemini-3-pro-image-preview

[output]
default_dir = ~/Posters
EOF
```

## 使用

```bash
python scripts/generate.py "海报标题" \
  --subtitle "副标题" \
  --content "内容项1" \
  --content "内容项2" \
  --cta "行动号召"
```

## 项目结构

```
bxz-poster-gen/
├── SKILL.md              # 技能定义文件
├── README.md             # 本文件
├── scripts/
│   └── generate.py       # 核心生成脚本
├── docs/
│   └── USAGE.md          # 详细使用说明
└── config/
    └── config.ini        # 配置文件模板
```

## License

MIT
