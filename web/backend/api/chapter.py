"""Chapter Challenge API Routes（封装 kugame 核心章节试炼系统）"""
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .deps import get_engine, persist

router = APIRouter(prefix="/api/chapter", tags=["chapter"])


class ChapterAnswerRequest(BaseModel):
    answer: Any  # 单选为字母，多选为字母列表，判断/填空为文本


@router.get("")
async def get_chapters():
    """获取所有开放章节及各关进度状态"""
    engine = get_engine()
    return {
        "status": "success",
        "data": engine.get_chapter_challenges(),
    }


@router.post("/{category}/tier/{tier}/start")
async def start_tier(category: str, tier: int):
    """开始一次章节闯关会话"""
    engine = get_engine()
    try:
        result = engine.start_chapter_tier(category, tier)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "无法开始关卡"))
    return {"status": "success", "data": result}


@router.get("/current")
async def current_question():
    """获取当前正在作答的题目（不含答案）"""
    engine = get_engine()
    question = engine.get_current_chapter_question()
    if not question:
        raise HTTPException(status_code=404, detail="没有进行中的章节答题")
    return {"status": "success", "data": question}


@router.post("/answer")
async def answer_question(request: ChapterAnswerRequest):
    """判答当前题目；最后一题时返回关卡结算"""
    engine = get_engine()
    result = engine.answer_current_chapter_question(request.answer)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "判题失败"))
    if result.get("finished"):
        persist()
    return {"status": "success", "data": result}
