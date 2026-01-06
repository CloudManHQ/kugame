"""游戏引擎

KuGame的核心游戏逻辑引擎，负责处理游戏状态管理、挑战生成、答案验证等核心功能。
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from .player import Player, Sect
from .story import StoryManager, Chapter
from .kubernetes_commands import KubernetesCommandManager, CommandCategory
import random


class GameState(Enum):
    """游戏状态枚举
    
    定义游戏的各种状态，用于状态管理和流程控制。
    """
    MENU = "menu"  # 主菜单
    STORY = "story"  # 故事模式
    PRACTICE = "practice"  # 练习模式
    CHALLENGE = "challenge"  # 挑战模式
    QUIZ = "quiz"  # 测验模式
    PROGRESS = "progress"  # 进度查看
    QUIT = "quit"  # 退出游戏


@dataclass
class Challenge:
    """挑战数据类
    
    表示游戏中的一个挑战任务，包含挑战的各种属性。
    
    Attributes:
        challenge_id: 挑战唯一标识
        title: 挑战标题
        description: 挑战描述
        question: 挑战问题
        expected_command: 预期的命令答案
        hint: 提示信息
        reward_exp: 完成挑战获得的经验值
        difficulty: 挑战难度（1-10）
    """
    challenge_id: str
    title: str
    description: str
    question: str
    expected_command: str
    hint: str
    reward_exp: int
    difficulty: int


class GameEngine:
    """游戏引擎
    
    负责游戏的核心逻辑，包括玩家管理、故事推进、挑战生成、答案验证等。
    
    Attributes:
        story_manager: 故事管理器，负责故事章节和剧情
        command_manager: Kubernetes命令管理器，负责命令验证和学习
        player: 当前玩家对象
        state: 当前游戏状态
        current_challenge: 当前正在进行的挑战
        score: 玩家总得分
        streak: 连续正确回答的次数
    """
    
    def __init__(self):
        """初始化游戏引擎"""
        self.story_manager = StoryManager()
        self.command_manager = KubernetesCommandManager()
        self.player: Optional[Player] = None
        self.state = GameState.MENU
        self.current_challenge: Optional[Challenge] = None
        self.score: float = 0.0
        self.streak: int = 0
    
    def initialize_player(self, name: str, sect: Sect) -> Player:
        """初始化玩家
        
        创建新玩家并保存到本地。
        
        Args:
            name: 玩家名称
            sect: 玩家选择的门派
            
        Returns:
            创建的玩家对象
        """
        if not name or not isinstance(name, str):
            raise ValueError("玩家名称必须是非空字符串")
        
        if not isinstance(sect, Sect):
            raise ValueError("门派必须是Sect枚举类型")
        
        self.player = Player(name=name, sect=sect)
        self.player.save()
        return self.player
    
    def load_player(self, filepath: str = "player_save.json") -> Optional[Player]:
        """加载玩家
        
        从本地文件加载玩家数据。
        
        Args:
            filepath: 加载文件路径，默认在当前目录
            
        Returns:
            加载的玩家对象，如果没有保存的玩家则返回None
        """
        self.player = Player.load(filepath)
        if self.player:
            # 确保当前章节有效
            try:
                self.story_manager.current_chapter = Chapter(self.player.current_chapter)
            except ValueError:
                self.story_manager.current_chapter = Chapter.序章
        return self.player
    
    def get_menu_options(self) -> List[Dict[str, str]]:
        """获取菜单选项
        
        返回游戏主菜单的选项列表。
        
        Returns:
            菜单选项列表，每个选项包含id、name和description
        """
        return [
            {"id": "story", "name": "📖 开始故事", "description": "继续阅读故事，学习Kubernetes命令"},
            {"id": "practice", "name": "⚔️ 修炼场", "description": "练习已学命令"},
            {"id": "challenge", "name": "🏆 挑战关卡", "description": "完成挑战任务"},
            {"id": "quiz", "name": "📝 知识问答", "description": "测试你的知识"},
            {"id": "progress", "name": "📊 修炼进度", "description": "查看学习进度"},
            {"id": "commands", "name": "📚 命令手册", "description": "查看所有命令"},
            {"id": "save", "name": "💾 保存进度", "description": "保存当前进度"},
            {"id": "quit", "name": "🚪 退出游戏", "description": "退出游戏"},
        ]
    
    def get_story_content(self) -> Dict[str, Any]:
        """获取当前故事内容
        
        返回当前章节的故事内容，包括介绍、叙述、概念和命令等。
        
        Returns:
            当前章节的故事内容字典
        """
        chapter = self.story_manager.get_current_chapter()
        return {
            "chapter_id": chapter.chapter_id.value,
            "title": chapter.title,
            "introduction": chapter.introduction,
            "narrative": chapter.narrative,
            "concepts": chapter.kubernetes_concepts,
            "commands": chapter.commands_to_learn,
            "reward_exp": chapter.reward_exp,
        }
    
    def generate_challenge(self) -> Optional[Challenge]:
        """生成挑战
        
        根据当前章节的命令生成一个挑战任务。
        
        Returns:
            生成的挑战对象，如果没有可用命令则返回None
        """
        chapter = self.story_manager.get_current_chapter()
        commands = chapter.commands_to_learn
        
        if not commands:
            return None
        
        target_command = random.choice(commands)
        cmd_info = self.command_manager.get_command(target_command)
        
        if not cmd_info:
            return None
        
        challenge_id = f"{chapter.chapter_id.value}_challenge_{random.randint(1000, 9999)}"
        
        # 计算难度，根据章节ID中的数字
        chapter_num = int(chapter.chapter_id.value.split('_')[-1]) if 'chapter_' in chapter.chapter_id.value else 0
        difficulty = min(10, chapter_num + 1)  # 限制难度在1-10之间
        
        challenge = Challenge(
            challenge_id=challenge_id,
            title=f"修炼挑战 - {cmd_info.kubernetes_concept}",
            description=f"掌握{cmd_info.description}的技巧",
            question=f"如何{cmd_info.description}？",
            expected_command=target_command,
            hint=f"使用 {cmd_info.syntax} 格式",
            reward_exp=chapter.reward_exp,
            difficulty=difficulty,
        )
        
        self.current_challenge = challenge
        return challenge
    
    def check_answer(self, user_answer: str) -> Dict[str, Any]:
        """检查答案
        
        验证用户输入的命令是否正确，并返回结果。
        
        Args:
            user_answer: 用户输入的命令
            
        Returns:
            包含验证结果的字典，包括是否正确、消息、连击数、得分和解锁成就等
        """
        if not self.current_challenge:
            return {"correct": False, "message": "没有正在进行的挑战"}
        
        if not isinstance(user_answer, str):
            return {"correct": False, "message": "答案必须是字符串类型"}
        
        user_answer = user_answer.strip()
        expected = self.current_challenge.expected_command
        
        is_correct = user_answer == expected
        unlocked_achievements = []
        
        if is_correct:
            self.streak += 1
            # 连击加成，最多5倍
            streak_bonus = min(5.0, 1.0 + self.streak * 0.1)
            self.score += self.current_challenge.reward_exp * streak_bonus
            
            if self.player:
                # 更新玩家数据
                self.player.complete_challenge(self.current_challenge.challenge_id)
                self.player.learn_command(expected)
                self.player.gain_experience(self.current_challenge.reward_exp)
                
                # 更新连续成功次数和统计数据
                self.player.update_streak(True)
                
                # 检查并解锁成就
                unlocked_achievements = self.player.check_and_unlock_achievements()
                
                # 更新玩家的streak属性
                self.player.streak = self.streak
        else:
            self.streak = 0
            if self.player:
                # 更新玩家的连续成功次数
                self.player.update_streak(False)
                self.player.streak = self.streak
        
        result = {
            "correct": is_correct,
            "streak": self.streak,
            "score": int(self.score),
            "unlocked_achievements": unlocked_achievements
        }
        
        if is_correct:
            result["message"] = f"✓ 回答正确！获得 {int(self.current_challenge.reward_exp)} 经验值"
            result["streak_bonus"] = streak_bonus
        else:
            result["message"] = f"✗ 回答错误。正确答案是: {expected}"
            result["hint"] = self.current_challenge.hint
            result["expected"] = expected
            result["given"] = user_answer
        
        return result
    
    def advance_chapter(self) -> bool:
        """推进章节
        
        推进到下一个故事章节。
        
        Returns:
            如果成功推进到下一章节则返回True，否则返回False
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法推进章节")
        
        if self.story_manager.advance_chapter():
            self.player.current_chapter = self.story_manager.current_chapter.value
            self.player.gain_experience(500)  # 章节奖励
            self.player.save()  # 自动保存进度
            return True
        return False
    
    def get_practice_commands(self) -> List[str]:
        """获取可练习的命令
        
        获取玩家已经掌握的命令列表，用于练习模式。
        
        Returns:
            可练习的命令列表
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取练习命令")
        
        mastered = set(self.player.kubectl_commands_mastered)
        all_commands = set(self.command_manager.get_all_commands())
        return sorted(list(mastered.intersection(all_commands)))
    
    def generate_quiz(self) -> Optional[Dict[str, Any]]:
        """生成测验
        
        生成一个知识测验，包含问题、选项、正确答案等。
        
        Returns:
            测验字典，如果没有足够的命令则返回None
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法生成测验")
        
        mastered = self.get_practice_commands()
        
        if not mastered:
            return {
                "question": "还没有掌握任何命令，请先完成故事章节",
                "options": [],
                "correct_index": -1,
                "explanation": "",
                "command": "",
                "concept": ""
            }
        
        target_command = random.choice(mastered)
        cmd_info = self.command_manager.get_command(target_command)
        
        if not cmd_info:
            return None
        
        # 生成干扰选项
        all_commands = self.command_manager.get_all_commands()
        potential_distractors = [c for c in all_commands if c != target_command]
        
        # 确保有足够的干扰选项
        if len(potential_distractors) < 3:
            distractors = potential_distractors
        else:
            distractors = random.sample(potential_distractors, 3)
        
        options = distractors + [target_command]
        random.shuffle(options)
        
        correct_index = options.index(target_command)
        
        return {
            "question": f"以下哪个命令用于：{cmd_info.description}？",
            "options": options,
            "correct_index": correct_index,
            "explanation": f"示例：{cmd_info.example}",
            "command": target_command,
            "concept": cmd_info.kubernetes_concept
        }
    
    def get_progress(self) -> Dict[str, Any]:
        """获取游戏进度
        
        获取玩家的游戏进度，包括等级、经验、章节进度、命令掌握情况和成就进度等。
        
        Returns:
            包含玩家进度的字典
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取进度")
        
        story_progress = self.story_manager.get_story_progress(self.player)
        command_report = self.command_manager.get_progress_report(
            self.player.kubectl_commands_mastered
        )
        achievement_progress = self.player.get_achievement_progress()
        
        player_progress = self.player.get_progress()
        
        return {
            "player": {
                "title": self.player.title,
                "level": player_progress["level"],
                "experience": player_progress["experience"],
                "required_exp": player_progress["required_exp"],
                "cultivation": self.player.cultivation.value,
                "custom_titles": self.player.custom_titles,
                "sect_bonus": self.player.sect_bonus,
                "total_correct": self.player.total_correct,
                "total_attempts": self.player.total_attempts,
                "accuracy": round(self.player.total_correct / self.player.total_attempts * 100, 1) if self.player.total_attempts > 0 else 0,
            },
            "story": story_progress,
            "commands": command_report,
            "achievements": achievement_progress,
            "total_score": int(self.score),
            "streak": self.streak,
        }
    
    def get_all_commands_info(self) -> List[Dict[str, Any]]:
        """获取所有命令信息
        
        获取所有Kubernetes命令的详细信息，包括语法、示例、描述等。
        
        Returns:
            命令信息列表
        """
        if not self.player:
            raise ValueError("玩家未初始化，无法获取命令信息")
        
        commands_info = []
        for cmd in self.command_manager.commands.values():
            commands_info.append({
                "name": cmd.name,
                "category": cmd.category.value,
                "description": cmd.description,
                "syntax": cmd.syntax,
                "example": cmd.example,
                "concept": cmd.kubernetes_concept,
                "mastered": cmd.name in self.player.kubectl_commands_mastered,
            })
        
        # 按分类排序
        commands_info.sort(key=lambda x: x["category"])
        return commands_info
    
    def save_game(self) -> bool:
        """保存游戏
        
        保存当前玩家的游戏进度到本地文件。
        
        Returns:
            如果保存成功则返回True，否则返回False
        """
        if not self.player:
            return False
        
        try:
            self.player.save()
            return True
        except Exception as e:
            # 记录保存失败日志（实际项目中可以使用日志系统）
            print(f"保存游戏失败: {str(e)}")
            return False
    
    def reset_streak(self) -> None:
        """重置连击
        
        重置连续正确回答的次数。
        """
        self.streak = 0
    
    def get_player(self) -> Optional[Player]:
        """获取当前玩家
        
        Returns:
            当前玩家对象，如果未初始化则返回None
        """
        return self.player
    
    def set_state(self, state: GameState) -> None:
        """设置游戏状态
        
        Args:
            state: 新的游戏状态
        """
        if not isinstance(state, GameState):
            raise ValueError("状态必须是GameState枚举类型")
        
        self.state = state
    
    def get_state(self) -> GameState:
        """获取当前游戏状态
        
        Returns:
            当前游戏状态
        """
        return self.state
