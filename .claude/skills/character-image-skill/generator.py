#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Character Image Prompt Generator
小说人物文生图提示词生成器

作者: Claude Code Assistant
版本: 1.0.0
功能: 根据小说大纲和人物小传生成高质量的人物角色文生图提示词
"""

import os
import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Character:
    """人物信息数据类"""
    name: str
    age: Optional[str] = None
    personality: Optional[str] = None
    appearance: Optional[str] = None
    clothing: Optional[str] = None
    background: Optional[str] = None
    other_features: Optional[str] = None


@dataclass
class NovelInfo:
    """小说信息数据类"""
    title: str
    genre: Optional[str] = None
    era: Optional[str] = None
    setting: Optional[str] = None
    world_view: Optional[str] = None
    atmosphere: Optional[str] = None


class CharacterImagePromptGenerator:
    """人物文生图提示词生成器"""

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化生成器

        Args:
            config: 配置参数字典
        """
        self.config = config or self._default_config()

        # 时代背景映射
        self.era_mapping = {
            "古代仙侠": {
                "style_tags": ["ancient Chinese style", "immortal cultivation", "ethereal", "mystical"],
                "clothing_keywords": ["robes", "hanfu", "silk", "embroidery", "jade pendant", "hair crown"]
            },
            "民国": {
                "style_tags": ["Republic of China era", "1920s-1940s", "Shanghai style", "vintage"],
                "clothing_keywords": ["cheongsam", "suit", "tweed", "fedora", "pearl necklace"]
            },
            "现代都市": {
                "style_tags": ["modern urban", "contemporary", "city life", "fashionable"],
                "clothing_keywords": ["business suit", "casual wear", "designer clothes", "accessories"]
            },
            "未来赛博朋克": {
                "style_tags": ["cyberpunk", "futuristic", "neon lights", "high-tech", "dystopian"],
                "clothing_keywords": ["cybernetic implants", "LED accessories", "synthetic materials", "tech wear"]
            }
        }

        # 性格映射
        self.personality_mapping = {
            "高冷孤傲": {
                "expression": "cold expression", "eyes": "icy gaze", "posture": "upright posture",
                "colors": ["cold tones", "monochrome", "deep blue", "silver"],
                "cn_expression": "冷漠表情", "cn_eyes": "冰冷眼神", "cn_posture": "挺拔姿态",
                "cn_colors": ["冷色调", "黑白灰", "深蓝", "银色"]
            },
            "活泼跳脱": {
                "expression": "bright smile", "eyes": "sparkling eyes", "posture": "dynamic pose",
                "colors": ["bright colors", "warm tones", "vibrant", "rainbow"],
                "cn_expression": "灿烂笑容", "cn_eyes": "灵动眼神", "cn_posture": "动态姿势",
                "cn_colors": ["明亮色彩", "暖色调", "活力四射", "彩虹色"]
            },
            "阴鸷腹黑": {
                "expression": "sly smile", "eyes": "deep mysterious eyes", "posture": "leaned posture",
                "colors": ["dark tones", "shadows", "deep purple", "black"],
                "cn_expression": "诡异笑容", "cn_eyes": "深邃神秘", "cn_posture": "微倾姿态",
                "cn_colors": ["暗色调", "阴影", "深紫", "黑色"]
            },
            "温柔善良": {
                "expression": "gentle smile", "eyes": "warm kind eyes", "posture": "graceful posture",
                "colors": ["soft colors", "pastel", "warm white", "light pink"],
                "cn_expression": "温柔笑容", "cn_eyes": "温暖善良", "cn_posture": "优雅姿态",
                "cn_colors": ["柔和色彩", "淡色", "暖白", "浅粉"]
            }
        }

    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "prompt_length": "detailed",
            "style_weight": 1.2,
            "character_limit": 5,
            "model_adapter": "midjourney",
            "background_inclusion": True,
            "personality_mapping": True,
            "detail_level": "high"
        }

    def parse_novel_outline(self, outline_path: str) -> NovelInfo:
        """
        解析小说大纲

        Args:
            outline_path: 大纲文件路径

        Returns:
            NovelInfo: 小说信息对象
        """
        try:
            with open(outline_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"大纲文件不存在: {outline_path}")

        # 提取小说标题
        title_match = re.search(r'#\s*([^\n]+)', content)
        title = title_match.group(1) if title_match else "未知小说"

        # 提取时代背景
        era_keywords = ["古代", "现代", "民国", "未来", "仙侠", "玄幻", "都市"]
        era = None
        for keyword in era_keywords:
            if keyword in content:
                era = keyword
                break

        # 提取故事背景和世界观
        setting_match = re.search(r'故事背景[：:]\s*([^\n]+)', content)
        setting = setting_match.group(1) if setting_match else None

        # 提取氛围风格
        atmosphere_keywords = ["黑暗", "光明", "热血", "治愈", "悬疑", "浪漫"]
        atmosphere = []
        for keyword in atmosphere_keywords:
            if keyword in content:
                atmosphere.append(keyword)

        return NovelInfo(
            title=title,
            era=era,
            setting=setting,
            atmosphere="、".join(atmosphere) if atmosphere else None
        )

    def parse_character_info(self, character_path: str) -> List[Character]:
        """
        解析人物小传

        Args:
            character_path: 人物文件路径

        Returns:
            List[Character]: 人物信息列表
        """
        try:
            with open(character_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"人物文件不存在: {character_path}")

        characters = []

        # 按人物分割内容
        character_sections = re.split(r'##\s*【([^】]+)】', content)[1:]

        for i in range(0, len(character_sections), 2):
            if i + 1 < len(character_sections):
                name = character_sections[i]
                section_content = character_sections[i + 1]

                character = Character(name=name)

                # 提取年龄
                age_match = re.search(r'年龄[：:]\s*([^\n]+)', section_content)
                if age_match:
                    character.age = age_match.group(1).strip()

                # 提取性格
                personality_match = re.search(r'性格[：:]\s*([^\n]+)', section_content)
                if personality_match:
                    character.personality = personality_match.group(1).strip()

                # 提取外貌
                appearance_match = re.search(r'外貌[：:]\s*([^\n]+)', section_content)
                if appearance_match:
                    character.appearance = appearance_match.group(1).strip()

                # 提取穿着
                clothing_match = re.search(r'穿着[：:]\s*([^\n]+)', section_content)
                if clothing_match:
                    character.clothing = clothing_match.group(1).strip()

                # 提取背景
                background_match = re.search(r'背景[：:]\s*([^\n]+)', section_content)
                if background_match:
                    character.background = background_match.group(1).strip()

                characters.append(character)

        return characters

    def generate_prompt_for_character(self, character: Character, novel_info: NovelInfo) -> Tuple[str, str]:
        """
        为单个人物生成中英文提示词

        Args:
            character: 人物信息
            novel_info: 小说信息

        Returns:
            Tuple[str, str]: (中文提示词, 英文提示词)
        """
        # 生成中文提示词
        cn_prompt_parts = []

        # 年龄和基本信息
        if character.age:
            cn_prompt_parts.append(f"一位{character.age}的{character.name}")
        else:
            cn_prompt_parts.append(f"一位{character.name}")

        # 外貌描述
        if character.appearance:
            cn_prompt_parts.append(character.appearance)
        else:
            # 默认外貌描述
            cn_prompt_parts.append("容貌俊美，五官精致")

        # 性格映射到神态
        if character.personality and self.config["personality_mapping"]:
            personality_key = next((key for key in self.personality_mapping.keys() if key in character.personality), None)
            if personality_key:
                personality_info = self.personality_mapping[personality_key]
                cn_prompt_parts.append(f"{personality_info['cn_expression']}，{personality_info['cn_eyes']}")

        # 穿着描述
        if character.clothing:
            cn_prompt_parts.append(f"身着{character.clothing}")
        else:
            # 根据时代背景生成默认穿着
            if novel_info.era and novel_info.era in self.era_mapping:
                era_info = self.era_mapping[novel_info.era]
                cn_prompt_parts.append(f"身着符合{novel_info.era}背景的服饰")

        # 发型和配饰
        if "长发" in (character.appearance or ""):
            cn_prompt_parts.append("长发飘逸")
        elif "短发" in (character.appearance or ""):
            cn_prompt_parts.append("短发利落")

        # 场景描述
        if self.config["background_inclusion"]:
            if character.background:
                cn_prompt_parts.append(f"背景是{character.background}")
            elif novel_info.setting:
                cn_prompt_parts.append(f"背景是{novel_info.setting}")

        # 风格标签
        cn_prompt_parts.append("8k超高清，细节拉满，高质量渲染")

        cn_prompt = "，".join(cn_prompt_parts) + "。"

        # 生成英文提示词
        en_prompt_parts = []

        # 年龄和基本信息
        if character.age:
            en_prompt_parts.append(f"A {character.age} named {character.name}")
        else:
            en_prompt_parts.append(f"A character named {character.name}")

        # 外貌描述
        if character.appearance:
            en_prompt_parts.append(self._translate_to_english(character.appearance))
        else:
            en_prompt_parts.append("beautiful face, delicate features")

        # 性格映射
        if character.personality and self.config["personality_mapping"]:
            personality_key = next((key for key in self.personality_mapping.keys() if key in character.personality), None)
            if personality_key:
                personality_info = self.personality_mapping[personality_key]
                en_prompt_parts.append(f"{personality_info['expression']}, {personality_info['eyes']}")

        # 穿着描述
        if character.clothing:
            en_prompt_parts.append(self._translate_to_english(character.clothing))
        elif novel_info.era and novel_info.era in self.era_mapping:
            era_info = self.era_mapping[novel_info.era]
            en_prompt_parts.append(f"wearing {novel_info.era} style clothing")

        # 场景描述
        if self.config["background_inclusion"]:
            if character.background:
                en_prompt_parts.append(self._translate_to_english(character.background))
            elif novel_info.setting:
                en_prompt_parts.append(self._translate_to_english(novel_info.setting))

        # 风格标签
        en_prompt_parts.append("8k ultra high definition, highly detailed, professional photography")

        # 添加模型特定参数
        if self.config["model_adapter"] == "midjourney":
            en_prompt_parts.append("--ar 3:4 --style raw --v 6")
        elif self.config["model_adapter"] == "stable-diffusion":
            en_prompt_parts.append("(masterpiece:1.2), best quality, highres")

        en_prompt = ", ".join(en_prompt_parts)

        return cn_prompt, en_prompt

    def _translate_to_english(self, chinese_text: str) -> str:
        """
        简单的中文到英文翻译（实际项目中应使用专业翻译API）

        Args:
            chinese_text: 中文文本

        Returns:
            str: 英文文本
        """
        # 这里是一个简化的翻译映射
        translation_map = {
            "古装": "ancient costume",
            "现代装": "modern clothing",
            "长发": "long hair",
            "短发": "short hair",
            "黑色": "black",
            "白色": "white",
            "红色": "red",
            "蓝色": "blue",
            "剑眉星目": "sword-like eyebrows and star-like eyes",
            "鼻梁高挺": "high nose bridge",
            "皮肤白皙": "fair skin",
            "身材修长": "slender figure",
            "气质出众": "outstanding temperament"
        }

        english_text = chinese_text
        for cn, en in translation_map.items():
            english_text = english_text.replace(cn, en)

        return english_text

    def generate_prompts(self, novel_info: NovelInfo, characters: List[Character]) -> str:
        """
        生成完整的人物提示词文档

        Args:
            novel_info: 小说信息
            characters: 人物列表

        Returns:
            str: 完整的Markdown文档内容
        """
        markdown_content = f"# {novel_info.title} 角色文生图提示词汇总\n\n"

        # 添加补充建议
        suggestions = self._generate_suggestions(characters)
        if suggestions:
            markdown_content += f"> 补充建议：{suggestions}\n\n"

        # 为每个人物生成提示词
        for character in characters:
            markdown_content += f"## 【{character.name}】\n\n"

            cn_prompt, en_prompt = self.generate_prompt_for_character(character, novel_info)

            markdown_content += "### 中文提示词\n"
            markdown_content += cn_prompt + "\n\n"

            markdown_content += "### 英文提示词\n"
            markdown_content += en_prompt + "\n\n"

        return markdown_content

    def _generate_suggestions(self, characters: List[Character]) -> Optional[str]:
        """
        生成补充建议

        Args:
            characters: 人物列表

        Returns:
            Optional[str]: 建议内容
        """
        suggestions = []

        for character in characters:
            if not character.appearance:
                suggestions.append(f"建议补充{character.name}的外貌描述")
            if not character.personality:
                suggestions.append(f"建议补充{character.name}的性格特征")
            if not character.clothing:
                suggestions.append(f"建议补充{character.name}的穿着偏好")

        if suggestions:
            return "；".join(suggestions[:3]) + "等，以生成更精准的提示词。"

        return None

    def save_to_file(self, content: str, novel_title: str, output_dir: str = "character-image") -> str:
        """
        保存提示词到文件

        Args:
            content: 文档内容
            novel_title: 小说标题
            output_dir: 输出目录

        Returns:
            str: 保存的文件路径
        """
        # 创建输出目录
        output_path = Path(output_dir) / novel_title
        output_path.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        filename = f"{novel_title}_角色文生图提示词汇总.md"
        file_path = output_path / filename

        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(file_path)


def main():
    """主函数示例"""
    generator = CharacterImagePromptGenerator()

    # 示例用法
    outline_path = "novels/xuanhuan/时劫管理局/outline.md"
    character_path = "novels/xuanhuan/时劫管理局/character.md"

    try:
        # 解析文件
        novel_info = generator.parse_novel_outline(outline_path)
        characters = generator.parse_character_info(character_path)

        # 生成提示词
        content = generator.generate_prompts(novel_info, characters)

        # 保存文件
        file_path = generator.save_to_file(content, novel_info.title)

        print(f"提示词已保存至: {file_path}")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()