"""Web 后端路由集成测试（验证封装 kugame 核心包后的真实行为）"""
# -*- coding: utf-8 -*-
import json
import os
import sys

import pytest

# fastapi/httpx 为 Web 后端可选依赖，缺失时跳过本模块
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient  # noqa: E402

# 将 web/backend 加入路径以导入 main
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND_DIR = os.path.join(_PROJECT_ROOT, "web", "backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

# 本地题库答案索引（后端 check 接口不再下发正确答案，测试自取）
with open(os.path.join(_PROJECT_ROOT, "complete_question_bank.json"), encoding="utf-8") as _f:
    _CORRECT_ANSWERS = {q["id"]: q["correct_answer"] for q in json.load(_f)["questions"]}


def _correct_answer(question_id: str):
    return _CORRECT_ANSWERS[question_id]


@pytest.fixture(scope="module")
def client():
    """共享 TestClient（引擎单例跨用例复用）"""
    import main
    with TestClient(main.app) as c:
        yield c


class TestWebBackendIntegration:
    """Web 后端封装 kugame 核心的集成验证"""

    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_player_info_from_core(self, client):
        """玩家信息来自真实引擎而非 mock"""
        resp = client.get("/api/player")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "level" in data
        assert "cultivation_realm" in data
        assert data["level"] >= 1

    def test_player_stats_from_core(self, client):
        resp = client.get("/api/player/stats")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "combat" in data
        assert "k8s" in data

    def test_create_player_invalid_sect(self, client):
        resp = client.post("/api/player/create", json={"name": "测试", "sect": "invalid"})
        assert resp.status_code == 400

    def test_create_player_valid(self, client):
        resp = client.post("/api/player/create", json={"name": "web测试侠", "sect": "qingyun"})
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["name"] == "web测试侠"
        assert data["sect"] == "青云宗"
        assert data["level"] == 1

    def test_k8s_commands_from_core(self, client):
        """命令手册来自核心命令管理器"""
        resp = client.get("/api/k8s/commands")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)
        assert len(data) > 0
        assert "name" in data[0]
        assert "proficiency" in data[0]

    def test_k8s_quiz(self, client):
        resp = client.get("/api/k8s/quiz")
        # 新玩家可能尚未掌握命令 -> 404 或返回测验
        assert resp.status_code in (200, 404)

    def test_questions_stats_from_core(self, client):
        """题库统计来自核心题库（含 P8 补充题）"""
        resp = client.get("/api/questions/stats")
        assert resp.status_code == 200
        stats = resp.json()
        assert stats["total_questions"] >= 600

    def test_game_question_and_answer_flow(self, client):
        """答题流程：出题 -> 判题，更新玩家数据"""
        resp = client.get("/api/game/question")
        assert resp.status_code == 200
        q = resp.json()["data"]
        qid = q["id"]
        assert "correct_answer" not in q  # 不泄题

        # 用题库真实答案判题（本地索引）
        ans = client.post("/api/game/answer", json={"question_id": qid, "answer": _correct_answer(qid)})
        assert ans.status_code == 200
        result = ans.json()["data"]
        assert result["correct"] is True
        assert result["exp_gained"] > 0

    def test_inventory_equipment_structure(self, client):
        resp = client.get("/api/inventory/equipment")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "equipped" in data
        assert "set_bonuses" in data

    def test_shop_items_from_core(self, client):
        """商店商品来自核心装备管理器"""
        resp = client.get("/api/shop/items")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)
        if data:
            assert "price" in data[0]
            assert "name" in data[0]

    def test_shop_buy_then_inventory(self, client):
        """购买装备后进入背包（需足够经验）"""
        # 先给玩家足够经验
        from api.deps import get_player
        player = get_player()
        player.experience += 100000

        items = client.get("/api/shop/items").json()["data"]
        assert items, "商店应有商品"
        item_id = items[0]["id"]

        buy = client.post("/api/shop/buy", json={"item_id": item_id})
        assert buy.status_code == 200

        inv = client.get("/api/inventory").json()["data"]["items"]
        assert any(i["id"] == item_id for i in inv)

    def test_combat_enemies_from_story(self, client):
        """敌人列表来自故事战斗事件"""
        resp = client.get("/api/combat/enemies")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert isinstance(data, list)
        assert len(data) > 0
        assert "name" in data[0]

    def test_combat_full_flow(self, client):
        """战斗流程：开始 -> 攻击"""
        enemies = client.get("/api/combat/enemies").json()["data"]
        enemy_id = enemies[0]["id"]

        start = client.post("/api/combat/start", json={"enemy_id": enemy_id})
        assert start.status_code == 200
        state = start.json()["data"]
        assert state["status"] == "combat_started"

        # 攻击：取一道题库题的正确答案保证命中
        q = client.get("/api/game/question").json()["data"]
        attack = client.post("/api/combat/attack", json={"answer": _correct_answer(q["id"])})
        assert attack.status_code == 200
        assert "combat" in attack.json()["data"]

    def test_chapter_list_six_chapters(self, client):
        """章节列表包含六章，进阶关默认锁定"""
        resp = client.get("/api/chapter")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert [c["category"] for c in data] == [
            "concepts", "network", "storage", "pod", "deployment", "security",
        ]
        for ch in data:
            assert ch["tiers"][1]["unlocked"] is False

    def test_chapter_locked_start_rejected(self, client):
        resp = client.post("/api/chapter/concepts/tier/2/start")
        assert resp.status_code == 400

    def test_chapter_unknown_category(self, client):
        resp = client.post("/api/chapter/nonexistent/tier/1/start")
        assert resp.status_code == 400

    def test_chapter_full_pass_flow(self, client):
        """答题流程：开始 -> 逐题答对 -> 结算与解锁"""
        start = client.post("/api/chapter/concepts/tier/1/start")
        assert start.status_code == 200
        assert start.json()["data"]["total"] == 10

        result = None
        while True:
            cur = client.get("/api/chapter/current")
            if cur.status_code == 404:
                break
            view = cur.json()["data"]
            answer = client.post(
                "/api/chapter/answer", json={"answer": _correct_answer(view["id"])}
            )
            assert answer.status_code == 200
            result = answer.json()["data"]
            assert "correct_answer" in result  # 判答后反馈正确答案与解析

        assert result["finished"] is True
        assert result["passed"] is True

        chapters = client.get("/api/chapter").json()["data"]
        concepts = next(c for c in chapters if c["category"] == "concepts")
        assert concepts["tiers"][0]["passed"] is True
        assert concepts["tiers"][1]["unlocked"] is True

    def test_chapter_answer_without_session(self, client):
        resp = client.post("/api/chapter/answer", json={"answer": "A"})
        assert resp.status_code == 400

    def test_check_endpoint_never_leaks_answer(self, client):
        """check 端点仅回判题结果，任何情况下不下发 correct_answer"""
        q = client.get("/api/game/question").json()["data"]
        for payload in ("A", "ZZZ"):
            resp = client.post(f"/api/questions/{q['id']}/check", json={"answer": payload})
            assert resp.status_code == 200
            assert "correct_answer" not in resp.json()
