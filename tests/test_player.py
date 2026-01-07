"""测试玩家角色系统

测试Player类的所有功能。
"""

import os
from kugame.player import Player, Sect, CultivationLevel


class TestPlayer:
    """测试Player类"""

    def test_player_initialization(self):
        """测试玩家初始化"""
        player = Player(name="测试侠客", sect=Sect.青云宗)

        assert player.name == "测试侠客"
        assert player.sect == Sect.青云宗
        assert player.level == 1
        assert player.experience == 0
        assert player.cultivation == CultivationLevel.凡人
        assert player.current_chapter == "序章"

    def test_player_initialization_default_name(self):
        """测试玩家默认名称"""
        player = Player(name="", sect=Sect.玄天宗)

        assert player.name == "无名侠客"

    def test_player_title(self):
        """测试玩家称号"""
        player = Player(name="剑心", sect=Sect.青云宗)

        assert player.title == "青云宗凡人之躯·剑心"

    def test_gain_experience(self):
        """测试获得经验"""
        player = Player(name="测试", sect=Sect.青云宗)
        initial_exp = player.experience

        player.gain_experience(50)

        # 考虑门派加成，青云宗加成1.1倍
        expected_exp = initial_exp + int(50 * player.sect_bonus)
        assert player.experience == expected_exp

    def test_level_up(self):
        """测试升级"""
        player = Player(name="测试", sect=Sect.青云宗)

        player.gain_experience(200)

        assert player.level > 1

    def test_cultivation_level_progression(self):
        """测试修炼境界进阶"""
        player = Player(name="测试", sect=Sect.青云宗)

        player.level = 25
        player._update_cultivation()

        assert player.cultivation == CultivationLevel.筑基期  # 21-30级对应筑基期

        # 测试金丹期
        player.level = 35
        player._update_cultivation()
        assert player.cultivation == CultivationLevel.金丹期  # 31-40级对应金丹期

    def test_learn_command(self):
        """测试学习命令"""
        player = Player(name="测试", sect=Sect.青云宗)
        initial_commands = len(player.kubectl_commands_mastered)

        player.learn_command("kubectl get pods")

        assert "kubectl get pods" in player.kubectl_commands_mastered
        assert len(player.kubectl_commands_mastered) == initial_commands + 1

    def test_learn_duplicate_command(self):
        """测试重复学习命令不增加经验"""
        player = Player(name="测试", sect=Sect.青云宗)

        player.learn_command("kubectl get pods")
        exp_after_first = player.experience

        player.learn_command("kubectl get pods")
        exp_after_second = player.experience

        assert exp_after_first == exp_after_second

    def test_complete_challenge(self):
        """测试完成挑战"""
        player = Player(name="测试", sect=Sect.青云宗)

        result = player.complete_challenge("test_challenge_1")

        assert result is True
        assert "test_challenge_1" in player.challenges_completed

    def test_complete_duplicate_challenge(self):
        """测试重复完成挑战"""
        player = Player(name="测试", sect=Sect.青云宗)

        player.complete_challenge("test_challenge_1")
        result = player.complete_challenge("test_challenge_1")

        assert result is False

    def test_to_dict(self):
        """测试转换为字典"""
        player = Player(name="测试", sect=Sect.青云宗)
        player.learn_command("kubectl run")

        data = player.to_dict()

        assert data["name"] == "测试"
        assert data["sect"] == "青云宗"
        assert "kubectl run" in data["kubectl_commands_mastered"]

    def test_save_and_load(self):
        """测试保存和加载"""
        player = Player(name="测试存档", sect=Sect.玄天宗)
        player.level = 5
        player.learn_command("kubectl get pods")

        test_path = "test_save.json"
        try:
            player.save(test_path)
            loaded_player = Player.load(test_path)

            assert loaded_player is not None
            assert loaded_player.name == "测试存档"
            assert loaded_player.sect == Sect.玄天宗
            assert loaded_player.level == 5
            assert "kubectl get pods" in loaded_player.kubectl_commands_mastered
        finally:
            if os.path.exists(test_path):
                os.remove(test_path)

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        result = Player.load("nonexistent.json")

        assert result is None

    def test_get_progress(self):
        """测试获取进度"""
        player = Player(name="测试", sect=Sect.青云宗)
        player.learn_command("kubectl get pods")

        progress = player.get_progress()

        assert "level" in progress
        assert "experience" in progress
        assert "commands_mastered" in progress
        assert progress["commands_mastered"] == 1


class TestSect:
    """测试门派枚举"""

    def test_sect_values(self):
        """测试门派值"""
        assert Sect.青云宗.value == "青云宗"
        assert Sect.玄天宗.value == "玄天宗"
        assert Sect.炼狱门.value == "炼狱门"
        assert Sect.逍遥派.value == "逍遥派"


class TestCultivationLevel:
    """测试修炼境界"""

    def test_cultivation_values(self):
        """测试境界值"""
        assert CultivationLevel.凡人.value[0] == 1
        assert CultivationLevel.练气期.value[0] == 2
        assert CultivationLevel.金丹期.value[0] == 4
        assert CultivationLevel.元婴期.value[0] == 5

    def test_cultivation_titles(self):
        """测试境界称号"""
        assert "凡人之躯" in CultivationLevel.凡人.value[1]
        assert "金丹大道" in CultivationLevel.金丹期.value[1]
