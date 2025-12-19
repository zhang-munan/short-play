---
name: character-image-skill
description: 小说人物文生图提示词生成技能包。根据小说大纲和人物小传，生成高质量的人物角色文生图提示词，支持单个人物或多人物批量处理，适配主流文生图模型（如Midjourney、Stable Diffusion）。
---

# Character Image Skill - 小说人物文生图提示词生成技能

## 技能描述
本技能专门用于根据小说大纲和人物小传，生成高质量的人物角色文生图提示词。支持单个人物或多人物批量处理，生成适配主流文生图模型（如Midjourney、Stable Diffusion）的中英文提示词。

## 核心功能
- **智能解析**: 自动分析小说大纲和人物小传，提取关键信息
- **背景适配**: 严格贴合小说的时代背景、故事环境和情节设定
- **性格映射**: 将人物性格特征融入外在形象描述
- **细节丰富**: 对长相、穿着、发型等进行高细节度描述
- **双语生成**: 同时生成中文和英文提示词，英文提示词适配主流模型

## 输入要求
- 小说大纲（outline.md）- 包含故事背景、时代设定、世界观等
- 人物小传（character.md）- 包含人物姓名、性格、外貌描述等

## 输出规范
- **文件路径**: `/character-image/<小说名>/`
- **文件格式**: Markdown (.md)
- **文件命名**: `[小说名]_角色文生图提示词汇总.md`
- **内容结构**: 按人物模块组织，包含中文提示词和英文提示词

## 提示词生成规则

### 1. 背景贴合规则
- 时代背景：古代仙侠、民国上海滩、未来赛博朋克等
- 环境设定：宗门、都市、秘境、废土等
- 氛围风格：清新洒脱、阴暗诡谲、科幻未来等

### 2. 性格映射规则
- 高冷孤傲 → 眼神淡漠、色调冷峻、姿态挺拔
- 活泼跳脱 → 眼神灵动、色彩鲜艳、动态姿势
- 阴鸷腹黑 → 眼神深邃、色调暗沉、神秘气质

### 3. 细节描述要求
- **长相**: 五官特征、脸型、肤色、神态表情
- **穿着**: 服饰款式、材质、颜色、装饰细节
- **发型**: 发色、发长、造型、配饰
- **体态**: 身材比例、姿态动作
- **道具**: 武器、饰品、标志性物品
- **场景**: 符合人物身份的环境背景

### 4. 英文提示词优化
- 使用标准英文描述词汇
- 添加风格标签（如: --ar 3:4, --style raw）
- 设置关键词权重（如: (detailed face:1.2)）
- 适配模型特性（Midjourney/SD）

## 输出模板示例

```markdown
# [小说名] 角色文生图提示词汇总

> 补充建议：根据当前人物信息，建议增加更多关于人物背景故事和性格细节的描述，以生成更精准的提示词。

## 【人物名1】

### 中文提示词
一位18岁的少年，剑眉星目，鼻梁高挺，唇线偏薄，肤色是常年习武的健康麦色，眼神桀骜不驯；身着玄色锦缎劲装，衣摆绣银色云纹，腰间系黑色皮质腰带，挂青铜兽纹玉佩；墨色长发束高马尾，红色发带系结，额前几缕碎发垂落；立于云梦莲花坞莲塘边，水面波光粼粼，整体氛围清新洒脱，古风仙侠风格，8k超高清，细节拉满。

### 英文提示词
A teenage boy of 18 years old, with sword-like eyebrows and star-like eyes, a high straight nose bridge, thin lip lines, healthy wheat-colored skin from years of martial arts practice, and unruly eyes; wearing a black brocade martial arts suit with silver cloud patterns embroidered on the hem, a black leather belt around the waist with a bronze beast-patterned jade pendant; long black hair tied into a high ponytail with a red hair band, a few broken hairs hanging down the forehead; standing by the lotus pond of Yunmeng Lianhuawu, sparkling water surface, fresh and free-spirited atmosphere, ancient immortal style, 8k ultra-high definition, full of details --ar 3:4 --style raw

## 【人物名2】

### 中文提示词
[人物2的中文提示词内容]

### 英文提示词
[人物2的英文提示词内容]
```

## 错误处理
- 输入文件不存在时给出明确提示
- 人物信息不完整时提供补充建议
- 文件路径问题自动创建目录
- Markdown格式错误自动修正

## 扩展功能
- 支持自定义提示词模板
- 支持不同风格标签预设
- 支持批量导出多种格式
- 支持提示词质量评估
