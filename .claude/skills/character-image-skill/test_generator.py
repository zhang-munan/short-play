#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证character-image-skill功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from generator import CharacterImagePromptGenerator

def test_skill():
    """测试技能功能"""
    print("🔧 开始测试Character Image Skill...")

    # 初始化生成器
    generator = CharacterImagePromptGenerator()

    # 示例文件路径
    outline_path = "examples/sample_input_outline.md"
    character_path = "examples/sample_input_character.md"

    try:
        print("📖 解析小说大纲...")
        novel_info = generator.parse_novel_outline(outline_path)
        print(f"✅ 小说标题: {novel_info.title}")
        print(f"   时代背景: {novel_info.era}")
        print(f"   故事设定: {novel_info.setting}")

        print("\n👥 解析人物信息...")
        characters = generator.parse_character_info(character_path)
        print(f"✅ 检测到 {len(characters)} 个人物:")
        for char in characters:
            print(f"   - {char.name} ({char.age or '年龄未知'})")

        print("\n🎨 生成提示词...")
        content = generator.generate_prompts(novel_info, characters)

        print("\n💾 保存文件...")
        output_path = generator.save_to_file(content, novel_info.title, "../../character-image")
        print(f"✅ 提示词已保存至: {output_path}")

        print("\n🎉 测试完成！功能正常")

        # 显示部分生成内容作为预览
        print("\n📋 生成内容预览:")
        print("=" * 50)
        lines = content.split('\n')
        for line in lines[:20]:  # 显示前20行
            print(line)
        if len(lines) > 20:
            print("...")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_skill()
    sys.exit(0 if success else 1)