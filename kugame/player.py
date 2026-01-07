"""玩家角色系统

定义玩家角色、属性、技能和成长体系，管理玩家的游戏进度和Kubernetes命令学习状态。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import os


class AchievementType(Enum):
    """成就类型枚举
    
    定义游戏中不同类型的成就。
    """
    命令掌握 = "command_mastery"   # 掌握命令相关成就
    故事进度 = "story_progress"     # 故事进度相关成就
    挑战完成 = "challenge_completion"  # 挑战完成相关成就
    连续成功 = "streak_success"     # 连续成功相关成就
    门派专精 = "sect_specialization"  # 门派专精相关成就


class Achievement:
    """成就类
    
    定义游戏中的成就，包含名称、描述、类型、条件和奖励。
    
    Attributes:
        id: 成就唯一标识
        name: 成就名称
        description: 成就描述
        achievement_type: 成就类型
        condition: 完成条件（如掌握命令数量、章节数等）
        reward: 奖励内容（经验值、称号等）
        unlocked: 是否已解锁
    """
    def __init__(self, id: str, name: str, description: str, achievement_type: AchievementType, condition: int, reward: dict):
        self.id = id
        self.name = name
        self.description = description
        self.type = achievement_type
        self.condition = condition
        self.reward = reward
        self.unlocked = False


class CultivationLevel(Enum):
    """修炼境界枚举
    
    定义玩家的修炼等级，每个等级对应不同的称号和能力。
    
    Attributes:
        value: 元组，包含等级数值和中文描述
    """
    凡人 = (1, "凡人之躯")       # 等级1-10
    练气期 = (2, "初步入门")       # 等级11-20
    筑基期 = (3, "根基稳固")       # 等级21-30
    金丹期 = (4, "金丹大道")       # 等级31-40
    元婴期 = (5, "元婴初成")       # 等级41-50
    化神期 = (6, "化神飞升")       # 等级51-60
    大乘期 = (7, "大乘圆满")       # 等级61-70
    渡劫期 = (8, "渡劫飞升")       # 等级71-80
    散仙 = (9, "逍遥天地")         # 等级81-90
    金仙 = (10, "金仙不朽")        # 等级91-100


class Sect(Enum):
    """门派枚举
    
    定义玩家可以选择的门派。
    """
    青云宗 = "青云宗"   # 正派，擅长基础扎实
    玄天宗 = "玄天宗"   # 中立，擅长变化多端
    炼狱门 = "炼狱门"   # 邪派，擅长爆发力强
    逍遥派 = "逍遥派"   # 散修，擅长灵活应变


@dataclass
class Player:
    """玩家角色类
    
    管理玩家的基本信息、修炼状态、学习进度和游戏成就。
    
    Attributes:
        name: 玩家名称
        sect: 玩家所属门派
        level: 当前等级
        experience: 当前经验值
        cultivation: 当前修炼境界
        skills: 掌握的技能列表
        achievements: 获得的成就列表
        achievement_objects: 成就对象列表（包含详细信息）
        current_chapter: 当前故事章节
        kubectl_commands_mastered: 掌握的Kubernetes命令列表
        challenges_completed: 完成的挑战列表
        streak: 连续正确回答次数
        total_correct: 总正确回答次数
        total_attempts: 总尝试次数
        custom_titles: 自定义称号列表
        sect_bonus: 门派加成
        
        # 战斗属性
        health: 当前生命值
        max_health: 最大生命值
        attack: 攻击力
        defense: 防御力
        
        # 答题系统
        wrong_commands: 答错的命令列表
    """
    name: str
    sect: Sect
    level: int = 1
    experience: int = 0
    cultivation: CultivationLevel = CultivationLevel.凡人
    skills: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    achievement_objects: List[Achievement] = field(default_factory=list)
    current_chapter: str = "序章"
    
    # Kubernetes学习进度
    kubectl_commands_mastered: List[str] = field(default_factory=list)
    challenges_completed: List[str] = field(default_factory=list)
    
    # 游戏统计数据
    streak: int = 0
    total_correct: int = 0
    total_attempts: int = 0
    
    # 自定义属性
    custom_titles: List[str] = field(default_factory=list)
    sect_bonus: float = 1.0
    
    # 战斗属性
    health: int = 100
    max_health: int = 100
    attack: int = 10
    defense: int = 5
    
    # 答题系统
    wrong_commands: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """初始化后处理
        
        确保玩家名称有效，设置默认值，初始化成就系统。
        """
        if not self.name:
            self.name = "无名侠客"
        
        # 确保属性类型正确
        if not isinstance(self.level, int) or self.level < 1:
            self.level = 1
        
        if not isinstance(self.experience, int) or self.experience < 0:
            self.experience = 0
        
        # 战斗属性初始化
        if not isinstance(self.health, int) or self.health < 0:
            self.health = 100
        if not isinstance(self.max_health, int) or self.max_health < 0:
            self.max_health = 100
        if not isinstance(self.attack, int) or self.attack < 0:
            self.attack = 10
        if not isinstance(self.defense, int) or self.defense < 0:
            self.defense = 5
        
        # 确保列表属性初始化正确
        if not isinstance(self.skills, list):
            self.skills = []
        
        if not isinstance(self.achievements, list):
            self.achievements = []
        
        if not isinstance(self.achievement_objects, list):
            self.achievement_objects = []
        
        if not isinstance(self.kubectl_commands_mastered, list):
            self.kubectl_commands_mastered = []
        
        if not isinstance(self.challenges_completed, list):
            self.challenges_completed = []
        
        if not isinstance(self.custom_titles, list):
            self.custom_titles = []
        
        if not isinstance(self.wrong_commands, list):
            self.wrong_commands = []
        
        if not isinstance(self.streak, int) or self.streak < 0:
            self.streak = 0
        
        if not isinstance(self.total_correct, int) or self.total_correct < 0:
            self.total_correct = 0
        
        if not isinstance(self.total_attempts, int) or self.total_attempts < 0:
            self.total_attempts = 0
        
        # 初始化成就系统
        self._initialize_achievements()
        
        # 设置门派加成
        self._set_sect_bonus()
        
        # 确保生命值不超过最大值
        if self.health > self.max_health:
            self.health = self.max_health
    
    def _initialize_achievements(self) -> None:
        """初始化成就系统
        
        创建所有预定义成就并添加到玩家的成就列表中。
        """
        # 如果成就已经初始化，跳过
        if self.achievement_objects:
            return
        
        # 预定义成就列表
        predefined_achievements = [
            # 命令掌握类成就
            Achievement(
                id="cmd_master_10",
                name="入门弟子",
                description="掌握10个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=10,
                reward={"experience": 500, "title": "命令初学者"}
            ),
            Achievement(
                id="cmd_master_30",
                name="熟练弟子",
                description="掌握30个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=30,
                reward={"experience": 1500, "title": "命令熟练者"}
            ),
            Achievement(
                id="cmd_master_50",
                name="命令专家",
                description="掌握50个Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=50,
                reward={"experience": 3000, "title": "命令专家"}
            ),
            Achievement(
                id="cmd_master_all",
                name="命令大师",
                description="掌握所有Kubernetes命令",
                achievement_type=AchievementType.命令掌握,
                condition=100,  # 设置为一个较大的值，实际会根据总命令数调整
                reward={"experience": 10000, "title": "Kubernetes命令大师"}
            ),
            
            # 故事进度类成就
            Achievement(
                id="story_chapter_3",
                name="初入江湖",
                description="完成第3章故事",
                achievement_type=AchievementType.故事进度,
                condition=3,
                reward={"experience": 1000, "title": "江湖新秀"}
            ),
            Achievement(
                id="story_chapter_6",
                name="江湖少侠",
                description="完成第6章故事",
                achievement_type=AchievementType.故事进度,
                condition=6,
                reward={"experience": 2500, "title": "江湖少侠"}
            ),
            Achievement(
                id="story_chapter_9",
                name="武林高手",
                description="完成第9章故事",
                achievement_type=AchievementType.故事进度,
                condition=9,
                reward={"experience": 5000, "title": "武林高手"}
            ),
            
            # 挑战完成类成就
            Achievement(
                id="challenge_10",
                name="挑战新手",
                description="完成10个挑战",
                achievement_type=AchievementType.挑战完成,
                condition=10,
                reward={"experience": 800, "title": "挑战新手"}
            ),
            Achievement(
                id="challenge_50",
                name="挑战达人",
                description="完成50个挑战",
                achievement_type=AchievementType.挑战完成,
                condition=50,
                reward={"experience": 4000, "title": "挑战达人"}
            ),
            
            # 连续成功类成就
            Achievement(
                id="streak_5",
                name="小有成就",
                description="连续正确回答5次",
                achievement_type=AchievementType.连续成功,
                condition=5,
                reward={"experience": 300, "title": "连击高手"}
            ),
            Achievement(
                id="streak_10",
                name="势如破竹",
                description="连续正确回答10次",
                achievement_type=AchievementType.连续成功,
                condition=10,
                reward={"experience": 800, "title": "连击大师"}
            ),
            Achievement(
                id="streak_20",
                name="无人能挡",
                description="连续正确回答20次",
                achievement_type=AchievementType.连续成功,
                condition=20,
                reward={"experience": 2000, "title": "连击王者"}
            ),
        ]
        
        self.achievement_objects = predefined_achievements
        # 检查并解锁已满足条件的成就
        self.check_and_unlock_achievements()
    
    def _set_sect_bonus(self) -> None:
        """设置门派加成
        
        根据玩家选择的门派设置不同的加成系数。
        """
        # 青云宗：基础扎实，经验加成
        if self.sect == Sect.青云宗:
            self.sect_bonus = 1.1
        # 玄天宗：变化多端，挑战加成
        elif self.sect == Sect.玄天宗:
            self.sect_bonus = 1.0
        # 炼狱门：爆发力强，连击加成
        elif self.sect == Sect.炼狱门:
            self.sect_bonus = 1.2
        # 逍遥派：灵活应变，学习加成
        elif self.sect == Sect.逍遥派:
            self.sect_bonus = 1.15
        else:
            self.sect_bonus = 1.0
    
    @property
    def title(self) -> str:
        """获取玩家称号
        
        根据门派和修炼境界生成玩家的完整称号。
        
        Returns:
            str: 玩家的完整称号
        """
        return f"{self.sect.value}{self.cultivation.value[1]}·{self.name}"
    
    def check_and_unlock_achievements(self) -> List[str]:
        """检查并解锁成就
        
        检查所有成就条件，解锁满足条件的成就，并返回解锁的成就列表。
        
        Returns:
            List[str]: 解锁的成就名称列表
        """
        unlocked_achievements = []
        
        for achievement in self.achievement_objects:
            if achievement.unlocked:
                continue
            
            # 根据成就类型检查条件
            if achievement.type == AchievementType.命令掌握:
                if len(self.kubectl_commands_mastered) >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)
            elif achievement.type == AchievementType.故事进度:
                # 假设章节ID格式为"第X章"
                try:
                    chapter_num = int(self.current_chapter.split("第")[1].split("章")[0])
                    if chapter_num >= achievement.condition:
                        self.unlock_achievement(achievement.id)
                        unlocked_achievements.append(achievement.name)
                except (IndexError, ValueError):
                    pass
            elif achievement.type == AchievementType.挑战完成:
                if len(self.challenges_completed) >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)
            elif achievement.type == AchievementType.连续成功:
                if self.streak >= achievement.condition:
                    self.unlock_achievement(achievement.id)
                    unlocked_achievements.append(achievement.name)
        
        return unlocked_achievements
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """解锁特定成就
        
        Args:
            achievement_id: 成就ID
            
        Returns:
            bool: 解锁成功返回True，否则返回False
        """
        for achievement in self.achievement_objects:
            if achievement.id == achievement_id and not achievement.unlocked:
                achievement.unlocked = True
                self.achievements.append(achievement.id)
                
                # 应用成就奖励
                if "experience" in achievement.reward:
                    self.gain_experience(achievement.reward["experience"])
                
                if "title" in achievement.reward:
                    self.custom_titles.append(achievement.reward["title"])
                
                return True
        return False
    
    def update_streak(self, correct: bool) -> None:
        """更新连续正确次数
        
        Args:
            correct: 是否回答正确
        """
        if correct:
            self.streak += 1
            self.total_correct += 1
        else:
            self.streak = 0
        
        self.total_attempts += 1
        
        # 检查连续成功成就
        self.check_and_unlock_achievements()
    
    def get_achievement_progress(self) -> Dict[str, Any]:
        """获取成就进度
        
        Returns:
            Dict[str, Any]: 成就进度字典
        """
        total_achievements = len(self.achievement_objects)
        unlocked_achievements = sum(1 for a in self.achievement_objects if a.unlocked)
        
        by_type = {}
        for achievement_type in AchievementType:
            type_achievements = [a for a in self.achievement_objects if a.type == achievement_type]
            type_unlocked = sum(1 for a in type_achievements if a.unlocked)
            by_type[achievement_type.value] = {
                "total": len(type_achievements),
                "unlocked": type_unlocked,
                "percentage": round(type_unlocked / len(type_achievements) * 100, 1) if type_achievements else 0
            }
        
        return {
            "total_achievements": total_achievements,
            "unlocked_achievements": unlocked_achievements,
            "progress_percentage": round(unlocked_achievements / total_achievements * 100, 1) if total_achievements else 0,
            "by_type": by_type,
            "achievement_list": [{"id": a.id, "name": a.name, "description": a.description, "unlocked": a.unlocked} 
                                for a in self.achievement_objects]
        }
    
    def gain_experience(self, exp: int) -> bool:
        """获得经验值，可能升级
        
        增加玩家经验值，如果达到升级条件则自动升级。
        应用门派加成。
        
        Args:
            exp: 获得的经验值
            
        Returns:
            bool: 如果发生升级则返回True，否则返回False
        """
        if not isinstance(exp, (int, float)) or exp < 0:
            raise ValueError("经验值必须是非负数")
        
        # 应用门派加成
        exp_with_bonus = int(exp * self.sect_bonus)
        self.experience += exp_with_bonus
        required_exp = self._calculate_required_exp()
        
        if self.experience >= required_exp:
            self.level_up()
            return True
        return False
    
    def _calculate_required_exp(self) -> int:
        """计算升级所需经验
        
        根据当前等级计算升级到下一等级所需的经验值。
        
        Returns:
            int: 升级所需的经验值
        """
        return int(100 * (1.5 ** (self.level - 1)))
    
    def level_up(self) -> None:
        """升级处理
        
        处理玩家升级逻辑，包括经验值消耗、等级提升和修炼境界更新。
        支持一次性升级多个等级。
        """
        while self.experience >= self._calculate_required_exp():
            self.experience -= self._calculate_required_exp()
            self.level += 1
            self._update_cultivation()
    
    def _update_cultivation(self) -> None:
        """根据等级更新修炼境界
        
        根据玩家当前等级，更新对应的修炼境界。
        
        等级对应关系：
        - 凡人：等级1-10
        - 练气期：等级11-20
        - 筑基期：等级21-30
        - 金丹期：等级31-40
        - 元婴期：等级41-50
        - 化神期：等级51-60
        - 大乘期：等级61-70
        - 渡劫期：等级71-80
        - 散仙：等级81-90
        - 金仙：等级91-100
        """
        # 按等级从高到低检查
        for cultivation in reversed(list(CultivationLevel)):
            if self.level >= cultivation.value[0] * 10 - 9:  # 调整等级对应关系
                self.cultivation = cultivation
                break
    
    def learn_command(self, command: str) -> bool:
        """学习命令
        
        记录玩家学习的Kubernetes命令，并给予经验奖励。
        
        Args:
            command: 学习的Kubernetes命令
            
        Returns:
            bool: 如果是新命令则返回True，否则返回False
        """
        if not isinstance(command, str) or not command:
            raise ValueError("命令必须是非空字符串")
        
        if command not in self.kubectl_commands_mastered:
            self.kubectl_commands_mastered.append(command)
            self.gain_experience(50)  # 学习命令获得50经验值
            return True
        return False
    
    def complete_challenge(self, challenge_id: str) -> bool:
        """完成挑战
        
        记录玩家完成的挑战，并给予经验奖励。
        
        Args:
            challenge_id: 挑战的唯一标识
            
        Returns:
            bool: 如果是新挑战则返回True，否则返回False
        """
        if not isinstance(challenge_id, str) or not challenge_id:
            raise ValueError("挑战ID必须是非空字符串")
        
        if challenge_id not in self.challenges_completed:
            self.challenges_completed.append(challenge_id)
            self.gain_experience(100)  # 完成挑战获得100经验值
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        将玩家对象转换为字典格式，用于保存和序列化。
        
        Returns:
            Dict[str, Any]: 玩家数据字典
        """
        return {
            "name": self.name,
            "sect": self.sect.value,
            "level": self.level,
            "experience": self.experience,
            "cultivation": self.cultivation.name,
            "skills": self.skills,
            "achievements": self.achievements,
            "achievement_objects": [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "type": a.type.value,
                    "condition": a.condition,
                    "reward": a.reward,
                    "unlocked": a.unlocked
                }
                for a in self.achievement_objects
            ],
            "current_chapter": self.current_chapter,
            "kubectl_commands_mastered": self.kubectl_commands_mastered,
            "challenges_completed": self.challenges_completed,
            "streak": self.streak,
            "total_correct": self.total_correct,
            "total_attempts": self.total_attempts,
            "custom_titles": self.custom_titles,
            "sect_bonus": self.sect_bonus,
        }
    
    def save(self, filepath: str = "player_save.json") -> bool:
        """保存玩家数据
        
        将玩家数据保存到本地文件。
        
        Args:
            filepath: 保存文件路径，默认在当前目录
            
        Returns:
            bool: 保存成功返回True，失败返回False
        """
        try:
            # 确保文件路径存在
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存玩家数据失败: {str(e)}")
            return False
    
    @classmethod
    def get_save_files(cls, directory: str = ".") -> List[str]:
        """获取所有存档文件列表
        
        Args:
            directory: 查找存档的目录，默认在当前目录
            
        Returns:
            List[str]: 存档文件列表
        """
        save_files = []
        try:
            # 遍历目录，查找以.json结尾的文件
            for file in os.listdir(directory):
                if file.endswith(".json"):
                    # 尝试加载文件，验证是否为有效的存档文件
                    filepath = os.path.join(directory, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # 验证必要字段
                            if all(field in data for field in ["name", "sect", "level", "experience"]):
                                save_files.append(file)
                    except (json.JSONDecodeError, ValueError, KeyError):
                        continue
        except Exception as e:
            print(f"获取存档文件列表失败: {str(e)}")
        return save_files
    
    @classmethod
    def delete_save(cls, filepath: str) -> bool:
        """删除指定存档
        
        Args:
            filepath: 要删除的存档文件路径
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"删除存档失败: {str(e)}")
            return False
    
    @classmethod
    def load(cls, filepath: str = "player_save.json") -> Optional["Player"]:
        """加载玩家数据
        
        从本地文件加载玩家数据。
        
        Args:
            filepath: 加载文件路径，默认在当前目录
            
        Returns:
            Optional[Player]: 加载的玩家对象，如果失败则返回None
        """
        try:
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证必要字段
            required_fields = ["name", "sect", "level", "experience"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"缺少必要字段: {field}")
            
            # 创建玩家对象
            # 安全获取修炼境界
            cultivation_name = data.get("cultivation", "凡人")
            try:
                cultivation = CultivationLevel[cultivation_name]
            except KeyError:
                # 如果获取失败，默认使用凡人
                cultivation = CultivationLevel.凡人
            
            player = cls(
                name=data["name"],
                sect=Sect(data["sect"]),
                level=int(data["level"]),
                experience=int(data["experience"]),
                cultivation=cultivation,
                skills=data.get("skills", []),
                achievements=data.get("achievements", []),
                current_chapter=data.get("current_chapter", "序章"),
                kubectl_commands_mastered=data.get("kubectl_commands_mastered", []),
                challenges_completed=data.get("challenges_completed", []),
                streak=data.get("streak", 0),
                total_correct=data.get("total_correct", 0),
                total_attempts=data.get("total_attempts", 0),
                custom_titles=data.get("custom_titles", []),
                sect_bonus=data.get("sect_bonus", 1.0),
            )
            
            # 加载成就对象
            if "achievement_objects" in data:
                player.achievement_objects = []
                for ach_data in data["achievement_objects"]:
                    ach_type = AchievementType(ach_data["type"])
                    achievement = Achievement(
                        id=ach_data["id"],
                        name=ach_data["name"],
                        description=ach_data["description"],
                        achievement_type=ach_type,
                        condition=ach_data["condition"],
                        reward=ach_data["reward"]
                    )
                    achievement.unlocked = ach_data["unlocked"]
                    player.achievement_objects.append(achievement)
            else:
                # 如果没有成就对象数据，初始化成就系统
                player._initialize_achievements()
            
            return player
        except FileNotFoundError:
            return None
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"加载玩家数据失败: {str(e)}")
            return None
    
    def get_progress(self) -> Dict[str, Any]:
        """获取学习进度
        
        返回玩家当前的学习进度和游戏状态。
        
        Returns:
            Dict[str, Any]: 包含当前进度信息的字典
        """
        return {
            "level": self.level,
            "experience": self.experience,
            "required_exp": self._calculate_required_exp(),
            "commands_mastered": len(self.kubectl_commands_mastered),
            "challenges_completed": len(self.challenges_completed),
            "cultivation": self.cultivation.name,
            "cultivation_title": self.cultivation.value,
        }
    
    def has_mastered_command(self, command: str) -> bool:
        """检查是否已掌握命令
        
        检查玩家是否已经掌握了指定的Kubernetes命令。
        
        Args:
            command: 要检查的命令
            
        Returns:
            bool: 如果已掌握则返回True，否则返回False
        """
        return command in self.kubectl_commands_mastered
    
    def has_completed_challenge(self, challenge_id: str) -> bool:
        """检查是否已完成挑战
        
        检查玩家是否已经完成了指定的挑战。
        
        Args:
            challenge_id: 要检查的挑战ID
            
        Returns:
            bool: 如果已完成则返回True，否则返回False
        """
        return challenge_id in self.challenges_completed
    
    def reset_progress(self) -> None:
        """重置进度
        
        重置玩家的学习进度，但保留基本信息（名称、门派）。
        """
        self.level = 1
        self.experience = 0
        self.cultivation = CultivationLevel.凡人
        self.skills = []
        self.achievements = []
        self.current_chapter = "序章"
        self.kubectl_commands_mastered = []
        self.challenges_completed = []
