"""章节试炼（按知识分类闯关）集成测试

覆盖：章节列表与解锁状态、锁定校验、通关流程、失败重试、
首通经验防重复、进度持久化。
"""
# -*- coding: utf-8 -*-
import pytest

from kugame.game_engine import GameEngine
from kugame.player import Player, Sect


@pytest.fixture()
def engine():
    """带新玩家的引擎（不读写存档文件）"""
    eng = GameEngine()
    eng.initialize_player("闯关测试侠", Sect.青云宗)
    return eng


def _answer_all_correct(engine) -> dict:
    """以题库真实答案答完当前会话全部题目，返回结算结果"""
    result = None
    while True:
        view = engine.get_current_chapter_question()
        if not view:
            break
        question = engine.question_bank.get_question(view["id"])
        assert question is not None
        result = engine.answer_current_chapter_question(question.correct_answer)
    assert result is not None and result["finished"]
    return result


class TestChapterChallenges:
    def test_lists_three_chapters_with_locked_tiers(self, engine):
        challenges = engine.get_chapter_challenges()

        assert [c["category"] for c in challenges] == ["concepts", "network", "storage"]
        for ch in challenges:
            assert ch["tiers"][0]["unlocked"] is True
            assert ch["tiers"][1]["unlocked"] is False  # 进阶需先通初窥
            assert ch["tiers"][2]["unlocked"] is False  # 登峰需先通进阶
            assert all(t["passed"] is False and t["stars"] == 0 for t in ch["tiers"])

    def test_menu_contains_chapter_entry(self, engine):
        option_ids = [opt["id"] for opt in engine.get_menu_options()]
        assert "chapter" in option_ids

    def test_unknown_category_raises(self, engine):
        with pytest.raises(ValueError):
            engine.start_chapter_tier("nonexistent_cat", 1)

    def test_locked_tier_rejected(self, engine):
        result = engine.start_chapter_tier("concepts", 2)
        assert result == {"success": False, "message": "请先通过初窥关卡"}


class TestChapterPassFlow:
    def test_pass_tier1_unlocks_tier2_and_grants_first_clear_exp(self, engine):
        start = engine.start_chapter_tier("concepts", 1)
        assert start["success"] is True
        assert start["total"] == GameEngine.TIER_QUESTIONS_TARGET
        assert start["target"] == 7  # 10题×70%

        exp_before = engine.player.experience
        exp_level = engine.player.level
        result = _answer_all_correct(engine)

        assert result["correct"] is True
        assert result["passed"] is True
        assert result["stars"] == 3  # 全对 → 三星
        assert result["exp_gained"] > 0
        assert result["first_clear"] is True
        # 经验可能触发升级，升级会消耗已计入的进阶经验
        total_exp_delta = (
            (engine.player.experience - exp_before)
            + max(0, engine.player.level - exp_level) * 100
        )
        assert total_exp_delta >= result["exp_gained"]

        progress = engine.player.chapter_progress["concepts"]
        assert progress["tiers"]["1"]["passed"] is True
        assert progress["highest_passed"] == 1

        concepts = next(c for c in engine.get_chapter_challenges() if c["category"] == "concepts")
        assert concepts["tiers"][1]["unlocked"] is True
        assert concepts["total_passed"] == 1

    def test_repeat_clear_grants_no_duplicate_exp(self, engine):
        for expected_first in (True, False):
            assert engine.start_chapter_tier("concepts", 1)["success"]
            result = _answer_all_correct(engine)
            assert result["passed"] is True
            assert result["first_clear"] is expected_first
            if expected_first:
                first_exp = result["exp_gained"]
        assert result["exp_gained"] == 0 and first_exp > 0

    def test_stars_never_decrease_on_best_run(self, engine):
        # 先拿三星
        engine.start_chapter_tier("concepts", 1)
        _answer_all_correct(engine)
        # 再混入错误答案：星级应保持历史最优
        engine.start_chapter_tier("concepts", 1)
        answered = 0
        while True:
            view = engine.get_current_chapter_question()
            if not view:
                break
            answer = "" if answered < 2 else engine.question_bank.get_question(view["id"]).correct_answer
            answered += 1
            engine.answer_current_chapter_question(answer)

        info = engine.player.chapter_progress["concepts"]["tiers"]["1"]
        assert info["stars"] == 3
        assert info["best_correct"] >= 7


class TestChapterFailFlow:
    def test_fail_keeps_progress_and_allows_retry(self, engine):
        exp_before = engine.player.experience

        assert engine.start_chapter_tier("network", 1)["success"]
        result = None
        while True:
            view = engine.get_current_chapter_question()
            if not view:
                break
            result = engine.answer_current_chapter_question("显然不会是这个答案zz")
        assert result["finished"] and result["passed"] is False and result["stars"] == 0
        assert engine.get_current_chapter_question() is None  # 会话已清理

        # 无经验奖励，进度只记录最佳战绩
        assert engine.player.experience == exp_before
        info = engine.player.chapter_progress["network"]["tiers"]["1"]
        assert info["passed"] is False
        assert info["best_correct"] == 0

        # 第2关依然锁定，第1关可重试
        network = next(c for c in engine.get_chapter_challenges() if c["category"] == "network")
        assert network["tiers"][1]["unlocked"] is False
        assert engine.start_chapter_tier("network", 1)["success"]

    def test_answer_without_session_rejected(self, engine):
        result = engine.answer_current_chapter_question("A")
        assert result == {"success": False, "message": "没有进行中的章节答题"}


class TestChapterPersistence:
    def test_progress_survives_save_load_roundtrip(self, engine, tmp_path):
        engine.start_chapter_tier("storage", 1)
        _answer_all_correct(engine)

        save_path = str(tmp_path / "chapter_save.json")
        assert engine.player.save(save_path) is True

        loaded_engine = GameEngine()
        player = loaded_engine.load_player(save_path)
        assert player is not None
        storage = next(
            c for c in loaded_engine.get_chapter_challenges() if c["category"] == "storage"
        )
        assert storage["tiers"][0]["passed"] is True
        assert storage["tiers"][1]["unlocked"] is True
        assert player.chapter_progress["storage"]["highest_passed"] == 1
