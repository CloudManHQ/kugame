#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证命令清单一致性的脚本
确保story.py中所有commands_to_learn列表中的命令都在KubernetesCommandManager的commands字典中存在
"""

from kugame.story import StoryManager
from kugame.kubernetes_commands import KubernetesCommandManager


def verify_command_consistency():
    """验证命令清单一致性"""
    print("开始验证命令清单一致性...")

    # 初始化StoryManager和KubernetesCommandManager
    story_manager = StoryManager()
    command_manager = KubernetesCommandManager()

    # 获取所有章节的命令
    all_story_commands = story_manager.get_all_commands()
    print(f"story.py中共有 {len(all_story_commands)} 个命令")

    # 获取KubernetesCommandManager中的所有命令
    all_manager_commands = command_manager.get_all_commands()
    print(f"KubernetesCommandManager中共有 {len(all_manager_commands)} 个命令")

    # 检查story.py中的命令是否都在KubernetesCommandManager中存在
    missing_commands = []
    for cmd in all_story_commands:
        if cmd not in command_manager.commands:
            missing_commands.append(cmd)

    if missing_commands:
        print(f"发现 {len(missing_commands)} 个命令在KubernetesCommandManager中不存在：")
        for cmd in missing_commands:
            print(f"  - {cmd}")
        return False
    else:
        print("✓ 所有story.py中的命令都在KubernetesCommandManager中存在")

    # 检查是否有重复的命令
    unique_story_commands = set(all_story_commands)
    if len(unique_story_commands) != len(all_story_commands):
        print(f"✗ 发现 {len(all_story_commands) - len(unique_story_commands)} 个重复命令")
        # 找出重复的命令
        from collections import Counter
        cmd_counter = Counter(all_story_commands)
        duplicate_commands = [cmd for cmd, count in cmd_counter.items() if count > 1]
        print("重复的命令：")
        for cmd in duplicate_commands:
            print(f"  - {cmd} (出现 {cmd_counter[cmd]} 次)")
    else:
        print("✓ 没有重复的命令")

    print("\n命令清单一致性验证完成！")
    return len(missing_commands) == 0


if __name__ == "__main__":
    success = verify_command_consistency()
    exit(0 if success else 1)
