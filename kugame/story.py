"""故事管理�?

管理武侠故事的章节、任务和剧情发展，增强故事趣味性，丰富人物设定和情节发展�?
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import random
from .player import Player


class Chapter(Enum):
    """故事章节枚举

    定义故事的各个章节，每个章节对应不同的故事内容和学习目标
    """
    序章 = "prologue"       # 入门介绍
    第一章 = "chapter_1"     # 容器基础
    第二章 = "chapter_2"     # 部署管理
    第三章 = "chapter_3"     # 服务发现
    第四章 = "chapter_4"     # 配置管理
    第五章 = "chapter_5"     # 存储管理
    第六章 = "chapter_6"     # 资源管理
    第七章 = "chapter_7"     # 故障排查
    第八章 = "chapter_8"     # 网络与安全
    第九章 = "chapter_9"     # 集群管理
    第十章 = "chapter_10"    # 云厂商管理
    第十一章 = "chapter_11"  # 云厂商高级特性
    终章 = "epilogue"        # 飞升大成


@dataclass
class Character:
    """故事人物数据�?

    存储故事中的人物信息，包括姓名、身份、性格特点等�?

    Attributes:
        name: 人物姓名
        identity: 人物身份
        personality: 人物性格
        dialogue_style: 对话风格
        relationship: 与玩家的关系
    """
    name: str
    identity: str
    personality: str
    dialogue_style: str
    relationship: str


@dataclass
class Monster:
    """怪物数据�?

    存储游戏中的怪物信息�?

    Attributes:
        name: 怪物名称
        health: 生命�?
        attack: 攻击�?
        defense: 防御�?
        experience_reward: 击败获得的经验�?
        command_challenge: 关联的命令挑�?
        description: 怪物描述
        level: 怪物等级
    """
    name: str
    health: int
    attack: int
    defense: int
    experience_reward: int
    command_challenge: Any
    description: str = ""
    level: int = 1


@dataclass
class StoryEvent:
    """故事事件数据�?

    存储故事中的随机事件信息�?

    Attributes:
        event_id: 事件ID
        title: 事件标题
        description: 事件描述
        choices: 选择列表
        consequences: 选择后果
        required_level: 触发所需等级
        rewards: 奖励信息
        event_type: 事件类型（normal, combat等）
        monster: 关联的怪物（如果是战斗事件�?
    """
    event_id: str
    title: str
    description: str
    choices: List[str]
    consequences: List[str]
    required_level: int = 1
    rewards: Dict[str, Any] = field(default_factory=dict)
    event_type: str = "normal"
    monster: Optional[Monster] = None


@dataclass
class StoryChapter:
    """故事章节数据�?

    存储故事章节的详细信息，包括标题、介绍、叙事、概念、命令等�?

    Attributes:
        chapter_id: 章节ID
        title: 章节标题
        introduction: 章节介绍
        narrative: 章节叙事内容
        kubernetes_concepts: 相关Kubernetes概念
        commands_to_learn: 本章节要学习的命�?
        challenge_id: 挑战ID
        reward_exp: 完成奖励经验
        characters: 出场人物列表
        events: 章节事件列表
        boss_fight: 是否�?boss �?
        ascii_image: ASCII图片，增强故事的视觉效果
    """
    chapter_id: Chapter
    title: str
    introduction: str
    narrative: str
    kubernetes_concepts: List[str]
    commands_to_learn: List[str]
    challenge_id: str
    reward_exp: int
    characters: List[Character] = field(default_factory=list)
    events: List[StoryEvent] = field(default_factory=list)
    boss_fight: bool = False
    ascii_image: Optional[str] = None

    @property
    def command_count(self) -> int:
        """获取本章节的命令数量"""
        return len(self.commands_to_learn)


class StoryManager:
    """故事管理�?

    管理武侠故事的章节、任务和剧情发展，提供故事内容、事件生成和进度跟踪功能�?

    Attributes:
        chapters: 章节字典
        current_chapter: 当前章节
        characters: 所有出场人�?
        random_events: 随机事件列表
    """
    chapters: Dict[Chapter, StoryChapter]
    current_chapter: Chapter
    characters: Dict[str, Character]
    random_events: List[StoryEvent]

    def __init__(self) -> None:
        self.characters = self._initialize_characters()
        self.random_events = self._initialize_random_events()
        self.chapters = self._initialize_chapters()
        self.current_chapter = Chapter.序章

    def _initialize_characters(self) -> Dict[str, Character]:
        """初始化故事人�?

        创建故事中所有出场的人物角色�?

        Returns:
            Dict[str, Character]: 人物字典
        """
        return {
            "掌门真人": Character(
                name="青云子",
                identity="青云宗掌门",
                personality="慈祥睿智，深谋远虑",
                dialogue_style="语重心长，充满哲理",
                relationship="师父"
            ),
            "大师兄": Character(
                name="李青峰",
                identity="青云宗大师兄，执法堂首座",
                personality="严肃认真，一丝不苟",
                dialogue_style="直接明了，严格要求",
                relationship="师兄"
            ),
            "二师兄": Character(
                name="王浩宇",
                identity="青云宗二师兄，外门执事",
                personality="热情开朗，乐于助人",
                dialogue_style="亲切友好，循循善诱",
                relationship="师兄"
            ),
            "三师姐": Character(
                name="林雨竹",
                identity="青云宗三师姐，藏经阁管理员",
                personality="温柔体贴，博学多才",
                dialogue_style="娓娓道来，详细耐心",
                relationship="师姐"
            ),
            "四师妹": Character(
                name="苏灵犀",
                identity="青云宗四师妹，炼丹阁弟子",
                personality="活泼可爱，古灵精怪",
                dialogue_style="俏皮灵动，充满活力",
                relationship="师妹"
            ),
            "魔教教主": Character(
                name="血魔",
                identity="炼狱门教主",
                personality="阴险狡诈，野心勃勃",
                dialogue_style="冷酷无情，充满威胁",
                relationship="敌人"
            ),
            "神秘人": Character(
                name="神秘人",
                identity="来历不明的修真者",
                personality="神秘莫测，亦正亦邪",
                dialogue_style="高深莫测，意味深长",
                relationship="中立"
            )
        }

    def _initialize_random_events(self) -> List[StoryEvent]:
        """初始化随机事�?

        创建游戏中可能触发的随机事件�?

        Returns:
            List[StoryEvent]: 随机事件列表
        """
        return [
            # 普通事�?
            StoryEvent(
                event_id="treasure_found",
                title="发现宝藏",
                description="你在宗门后山修炼时，意外发现了一个隐藏的宝箱�?,
                choices=["打开宝箱", "上报宗门", "离开此地"],
                consequences=[
                    "你打开了宝箱，发现了一本修炼秘籍！获得�?00经验值！",
                    "你将宝箱上报宗门，掌门真人赞赏你的诚实，奖励�?0经验值！",
                    "你决定不惹麻烦，离开了此地�?
                ],
                required_level=1,
                rewards={
                    "0": {"experience": 100},
                    "1": {"experience": 50}
                }
            ),
            StoryEvent(
                event_id="disciple_quarrel",
                title="弟子争执",
                description="你遇到两个弟子正在争执，他们都认为自己的Kubernetes命令是正确的�?,
                choices=["调解争执", "支持大师兄派", "支持二师兄派"],
                consequences=[
                    "你成功调解了争执，两人都向你道谢。获得了80经验值！",
                    "你支持了大师兄派，大师兄对你好感度提升。获得了50经验值！",
                    "你支持了二师兄派，二师兄对你好感度提升。获得了50经验值！"
                ],
                required_level=3,
                rewards={
                    "0": {"experience": 80},
                    "1": {"experience": 50},
                    "2": {"experience": 50}
                }
            ),
            StoryEvent(
                event_id="mysterious_visitor",
                title="神秘访客",
                description="一位神秘访客来到宗门，想要挑战你的Kubernetes知识�?,
                choices=["接受挑战", "拒绝挑战", "请教访客"],
                consequences=[
                    "你接受了挑战，成功击败了访客！获得了150经验值！",
                    "你拒绝了挑战，访客失望地离开了�?,
                    "你向访客请教，学到了不少新知识。获得了30经验值！"
                ],
                required_level=5,
                rewards={
                    "0": {"experience": 150},
                    "2": {"experience": 30}
                }
            ),

            # 战斗事件
            StoryEvent(
                event_id="monster_attack_pod",
                title="Pod魔袭�?,
                description="一只Pod魔突然从虚空中出现，它不断吞噬周围的资源，你必须阻止它！",
                choices=["战斗", "逃跑"],
                consequences=[
                    "你与Pod魔展开了激烈的战斗�?,
                    "你选择了逃跑，Pod魔在身后穷追不舍�?
                ],
                required_level=2,
                event_type="combat",
                monster=Monster(
                    name="Pod�?,
                    health=50,
                    attack=8,
                    defense=2,
                    experience_reward=100,
                    command_challenge="kubectl get pods",
                    description="由失控的Pod转化而成的怪物，喜欢吞噬资�?,
                    level=2
                )
            ),
            StoryEvent(
                event_id="monster_deployment",
                title="Deployment巨兽",
                description="一只巨大的Deployment巨兽正在破坏宗门的部署，它能够不断分裂出Pod魔！",
                choices=["战斗", "寻找支援"],
                consequences=[
                    "你勇敢地与Deployment巨兽展开了战斗！",
                    "你去寻找同门支援，回来时Deployment巨兽已经破坏了更多部署！"
                ],
                required_level=5,
                event_type="combat",
                monster=Monster(
                    name="Deployment巨兽",
                    health=120,
                    attack=15,
                    defense=5,
                    experience_reward=250,
                    command_challenge="kubectl scale deployment",
                    description="由失控的Deployment转化而成的巨兽，能够不断分裂",
                    level=5
                )
            ),
            StoryEvent(
                event_id="monster_service",
                title="Service幽灵",
                description="一只Service幽灵正在干扰宗门的网络，导致服务无法正常通信�?,
                choices=["战斗", "修复网络"],
                consequences=[
                    "你与Service幽灵展开了激烈的战斗�?,
                    "你尝试修复网络，但Service幽灵不断干扰你的工作�?
                ],
                required_level=8,
                event_type="combat",
                monster=Monster(
                    name="Service幽灵",
                    health=80,
                    attack=12,
                    defense=3,
                    experience_reward=200,
                    command_challenge="kubectl get services",
                    description="由故障的Service转化而成的幽灵，干扰网络通信",
                    level=8
                )
            ),

            # 其他事件
            StoryEvent(
                event_id="sword_dojo",
                title="剑冢试炼",
                description="你来到了宗门的剑冢试炼场，这里有各种Kubernetes命令的剑谱等待你挑战�?,
                choices=["挑战初级剑谱", "挑战中级剑谱", "挑战高级剑谱"],
                consequences=[
                    "你轻松完成了初级剑谱挑战！获得了50经验值！",
                    "你花费了一些时间，终于完成了中级剑谱挑战！获得�?20经验值！",
                    "高级剑谱异常艰难，你勉强通过，获得了200经验值和稀有称号！"
                ],
                required_level=7,
                rewards={
                    "0": {"experience": 50},
                    "1": {"experience": 120},
                    "2": {"experience": 200, "title": "剑谱大师"}
                }
            ),
            StoryEvent(
                event_id="crisis_at_gate",
                title="山门危机",
                description="魔教弟子突然袭击山门，你需要立即采取行动！",
                choices=["正面迎敌", "迂回包抄", "通知师兄师姐"],
                consequences=[
                    "你正面迎敌，虽然受伤，但成功击退了敌人！获得�?00经验值！",
                    "你迂回到敌人身后，发动突袭，获得�?0经验值和大师兄的赞赏�?,
                    "你通知了师兄师姐，大家一起轻松击退了敌人！获得�?0经验值！"
                ],
                required_level=9,
                rewards={
                    "0": {"experience": 100},
                    "1": {"experience": 80},
                    "2": {"experience": 50}
                }
            )
        ]

    def _initialize_chapters(self) -> Dict[Chapter, StoryChapter]:
        """初始化所有章�?

        创建故事的所有章节，包括章节内容、概念、命令和人物�?

        Returns:
            Dict[Chapter, StoryChapter]: 章节字典
        """
        return {
            Chapter.序章: StoryChapter(
                chapter_id=Chapter.序章,
                title="踏入仙门",
                introduction="凡人之躯，亦可问道苍穹。你站在青云宗山门前，心中充满对修真大道的好奇与向往�?,
                narrative="""
                青云宗，乃修真界第一大宗，以"道法自然，容器之�?闻名于世。宗门建在云海之上，
                弟子们修炼的是将万物化为容器的神通，可随心所欲地操控各种资源�?

                山门前，一位白发苍苍的老者正在清扫落叶。他抬头看了你一眼，眼中闪过一丝精光：
                "年轻人，你可见过那云端之上的仙境�?

                "弟子未曾见过，但心向往之�?你恭敬地回答�?

                老者微微一笑："要想踏入仙境，需先学�?容器�?之术。此术可将万物装入方寸之间，
                随取随用，来去自如。我是青云宗的掌门青云子，你可愿拜入我门下？"

                你毫不犹豫地跪下�?弟子愿意�?

                青云子满意地点点头，手中拂尘一挥，一行金色文字浮现空中：

                ┌─────────────────────────────────────────────────────────�?
                �?                   容器化入门心�?                        �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl run nginx --image=nginx                        �?
                �? （创建名为nginx的容器，如意金箍棒般随心所欲）             �?
                └─────────────────────────────────────────────────────────�?

                "此乃'kubectl run'心法，可创建世间万物。去吧，在心中默念此咒，
                感受容器化之术的奇妙。待你掌握此术，便正式成为我青云宗的弟子�?
                """,
                kubernetes_concepts=["容器化基础", "Pod概念", "容器运行"],
                commands_to_learn=["kubectl run", "kubectl get pods", "kubectl describe pod"],
                challenge_id="prologue_challenge",
                reward_exp=200,
                characters=[self.characters["掌门真人"]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
    ______  __  __  ______  ______  __  __  ______  __  __  ______  ______
   /\  ___\/\ \/\ \/\  ___\/\  ___\/\ \/\ \/\  ___\/\ \/\ \/\  ___\/\  ___\
   \ \  __\\ \ \ \ \ \___  \ \  __\\ \ \ \ \ \___  \ \ \_\ \ \  __\\ \  __\
    \ \_____\ \_____\/\_____\/\_____\/\_\/\_\/\_____\/\_____\/\_____\/\_____
     \/_____/\/_____/\/_____/\/_____/\/_/\/_/\/_____/\/_____/\/_____/\/_____

        ___   __   __   __   __   __   __   __   __   __   __   __   __   __
       /\_ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \ /\ \
       \//\ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \ \\ \\ \
         \_\ \\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \_\\ \
          \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/ \/_/

           /\  \ /\  \ /\  \ /\  \ /\  \ /\  \ /\  \ /\  \ /\  \ /\  \ /\  \
           \:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \
            \:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \\:\  \
             \:\  \\:\__\\:\__\\:\__\\:\__\\:\__\\:\__\\:\__\\:\__\\:\__\\:\__\
              \:\__\/\\__\\/__\\/__\\/__\\/__\\/__\\/__\\/__\\/__\\/__\\/__\
               \/__/ \/__/ \/__/ \/__/ \/__/ \/__/ \/__/ \/__/ \/__/ \/__/

                  _______  _______  _______  _______  _______
                 /\______\/\______\/\______\/\______\/\______\
                 \/______/\/______/\/______/\/______/\/______/

                     ______  ______  ______  ______  ______
                    /\  ___\/\  ___\/\  ___\/\  ___\/\  ___\
                    \ \  __\\ \  __\\ \  __\\ \  __\\ \  __\
                     \ \_____\ \_____\ \_____\ \_____\ \_____
                      \/_____/\/_____/\/_____/\/_____/\/_____

                          /\  \ /\  \ /\  \ /\  \ /\  \
                          \/_/ \/_/ \/_/ \/_/ \/_/ \/_/

                    一位白发苍苍的老者正在清扫落�?..
                """
            ),

            Chapter.第一�? StoryChapter(
                chapter_id=Chapter.第一�?
                title="容器之道",
                introduction="初入青云宗，你开始学习容器化之术的基础�?,
                narrative="""
                三个月后，你已经掌握了创建容器的基本方法。这一日，掌门真人召集众弟子：

                "近日魔教蠢蠢欲动，我们需要建立更强大的防御体系。众弟子听令�?
                需掌握'部署'之术，方能守护宗门安全�?

                二师兄王浩宇走到你面前，拍了拍你的肩膀�?
                "小师弟，容器只是个体，如同散兵游勇；部署才是军队，能够协同作战�?
                让我教你'Deployment'之道，这是成为将帅的基础�?

                二师兄说着，手中出现一面令旗，挥了挥令旗，地面上出现了整齐排列的士兵：

                ┌─────────────────────────────────────────────────────────�?
                �?                   部署军队心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl create deployment web --image=nginx            �?
                �? （创建名为web的部署军队，永不退缩）                      �?
                �?                                                        �?
                �? kubectl scale deployment web --replicas=3              �?
                �? （扩编军队至三人，齐心协力）                             �?
                └─────────────────────────────────────────────────────────�?

                "记住，一个好的将军不仅要能创建士兵，更要懂得如何管理和调度他们�?
                Deployment就像是你的中军大帐，通过它你可以指挥千军万马�?
                """,
                kubernetes_concepts=["Deployment", "ReplicaSet", "副本管理", "Pod模板"],
                commands_to_learn=["kubectl create deployment", "kubectl scale", "kubectl get deployments", "kubectl rollout status"],
                challenge_id="chapter_1_challenge",
                reward_exp=300,
                characters=[self.characters["掌门真人"], self.characters["二师�?]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
               ______  __   __  ______  ______  __   __  ______  __   __  ______  ______
              /\  ___\/\ "-.\ \  __ \/\  ___\/\ \ /\ \/\  ___\/\ "-.\ \  __ \/\  ___\
              \ \  __\\ \ \-.  \\ \ \ \ \  __\\ \ \'\ \ \  __\\ \ \-.  \\ \ \ \ \  __\\
               \ \_____\ \_\\"\_\\ \__\\ \_____\ \___\_\ \_____\ \_\\"\_\\ \__\\ \_____
                \/_____/\/_/ \/_/ \/_/ \/_____/\/___/_/ \/_____/\/_/ \/_/ \/_/ \/_____

            __   __  ______  ______  __   __  ______  ______  __   __  ______  ______
           /\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\/\  __ \/\ "-.\ \  __ \/\  ___\
           \ \ \-.  \\  __ \/\ \ \ \ \ \'\ \ \  __\\ \  __ \/\ \-.  \\  __ \/\  __\\
            \ \_\\"\_\\ \____\\ \____\\ \___\_\ \_____\ \_____\ \_\\"\_\\ \____\\ \_____
             \/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/\/_____/\/_/ \/_/ \/_____\/_____

                ________  ________  ________  ________  ________  ________  ________
               /\   ____\/\   __  \/\   ____\/\   ____\/\   __  \/\   __  \/\   ____\
               \ \  \___\/\  \ \  \/\ \  \___\/\  \___\/\  \ \  \/\  \ \  \/\ \  \___\
                \ \  \  \/\  \ \  \/\ \  \  \/\ \  \  \/\  \ \  \/\  \ \  \/\ \  \  \
                 \ \  \__\/\  \ \__\/\ \  \__\/\ \  \__\/\  \ \__\/\  \ \__\/\ \  \__\
                  \ \_____\/\__\/__\/\__\/\_____\/\_____\/\__\/__\/\__\/__\/\__\
                   \/_____/\/__/\/__/\/__/\/_____/\/_____\/\/__/\/__/\/__/\/__/\/__/

                       ______  ______  ______  ______  ______  ______  ______  ______
                      /\  __ \/\  ___\/\  ___\/\  __ \/\  __ \/\  ___\/\  ___\
                      \ \  __ \/\ \__ \/\ \__ \/\ \ \ \ \  __ \/\ \__ \/\  __\\
                       \ \_____\/\_____\/\_____\/\ \__\/\ \_____\/\_____\/\_____
                        \/_____/\/_____/\/_____/\/____/\/_____/\/_____/\/_____

                           ______  __   __  ______  ______  __   __  ______  ______
                          /\  __ \/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\/\  ___\
                          \ \  __\\ \ \-.  \\ \ \ \ \  __\\ \ \'\ \ \  __\\ \  __\\
                           \ \_____\ \_\\"\_\\ \__\\ \_____\ \___\_\ \_____\ \_____
                            \/_____/\/_/ \/_/ \/_/ \/_____/\/___/_/ \/_____/\/_____
                """
            ),

            Chapter.第二�? StoryChapter(
                chapter_id=Chapter.第二�?
                title="服务之门",
                introduction="掌握了部署术后，你需要学会如何让服务对外暴露�?,
                narrative="""
                你已经能够创建和管理部署军队，但新的问题随之而来�?

                这一日，宗门突然响起急促的钟声："报——！魔教来袭�?

                大师兄李青峰立即下令�?启动护山大阵！让外界能访问我们的服务�?
                小师弟，你负责开启宗门的服务之门�?

                你疑惑地问："如何让外界访问我们的服务�?

                大师兄解释道�?这便需�?Service'之术。Service是容器的门徒�?
                负责将外界的请求引导至正确的Pod。就如同宗门的迎客弟子，
                引导来访者前往正确的殿堂�?

                大师兄说着，手中出现一扇金色的门：

                ┌─────────────────────────────────────────────────────────�?
                �?                   服务暴露心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl expose deployment web --port=80 --type=NodePort�?
                �? （开启服务之门，让外界可访）                             �?
                �?                                                        �?
                �? kubectl get svc                                        �?
                �? （查看服务之门的状态）                                   �?
                └─────────────────────────────────────────────────────────�?

                "Service有三种形态：ClusterIP（内部通道）、NodePort（外部通道�?
                和LoadBalancer（天地之桥）。根据需要选择合适的形态�?
                现在，用你学到的Service之术，开启宗门的防御大阵�?
                """,
                kubernetes_concepts=["Service", "端口映射", "负载均衡", "网络暴露"],
                commands_to_learn=["kubectl expose", "kubectl get services", "kubectl describe service", "kubectl delete service"],
                challenge_id="chapter_2_challenge",
                reward_exp=350,
                characters=[self.characters["大师�?]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                _______  _______  _______  _______  _______  _______  _______  _______
               /\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \
               \//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /
                    / /     / /     / /     / /     / /     / /     / /     / /     / /
                   / /     / /     / /     / /     / /     / /     / /     / /     / /
                  / /     / /     / /     / /     / /     / /     / /     / /     / /
                 / /     / /     / /     / /     / /     / /     / /     / /     / /
                / /     / /     / /     / /     / /     / /     / /     / /     / /
               / /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /
               \//_____/\//_____/\//_____/\//_____/\//_____/\//_____/\//_____/\//

                      /\      /\      /\      /\      /\      /\      /\      /\      /\
                     /  \    /  \    /  \    /  \    /  \    /  \    /  \    /  \    /  \
                    /    \  /    \  /    \  /    \  /    \  /    \  /    \  /    \  /    \
                   /______\/______\/______\/______\/______\/______\/______\/______\/______\
                  |      |      |      |      |      |      |      |      |      |      |
                  |      |      |      |      |      |      |      |      |      |      |
                  |______|______|______|______|______|______|______|______|______|______|
                   \    /\    /\    /\    /\    /\    /\    /\    /\    /\    /\    /
                    \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \  /  \
                     \/    \/    \/    \/    \/    \/    \/    \/    \/    \/    \/

                _______  _______  _______  _______  _______  _______  _______  _______
               /\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \/\_____ \
               \//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /\//___/ /
                    / /     / /     / /     / /     / /     / /     / /     / /     / /
                   / /     / /     / /     / /     / /     / /     / /     / /     / /
                  / /     / /     / /     / /     / /     / /     / /     / /     / /
                 / /     / /     / /     / /     / /     / /     / /     / /     / /
                / /     / /     / /     / /     / /     / /     / /     / /     / /
               / /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /_____/ /
               \//_____/\//_____/\//_____/\//_____/\//_____/\//_____/\//_____/\//
                """
            ),

            Chapter.第三�? StoryChapter(
                chapter_id=Chapter.第三�?
                title="配置之密",
                introduction="真正的强者懂得如何灵活配置，而非硬编码�?,
                narrative="""
                战争日益激烈，你需要管理更多的配置信息。这一日，掌门真人召见你：

                "徒儿，你已学会创建服务，但若每次修改配置都要重新创建Pod�?
                岂不劳民伤财？今日本座传授你'ConfigMap'�?Secret'之术�?

                掌门真人说着，手中出现两个神秘的卷轴�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   配置管理心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl create configmap app-config --from-literal=key1�?
                �? =value1 --from-file=config.yaml                        �?
                �? （创建配置密卷，记录天地法则�?                          �?
                �?                                                        �?
                �? kubectl create secret generic db-secret \             �?
                �?     --from-literal=password=mypassword                 �?
                �? （创建机密密钥，守护重要信息�?                          �?
                �?                                                        �?
                �? kubectl get configmaps                                 �?
                �? （查看配置密卷）                                        �?
                └─────────────────────────────────────────────────────────�?

                "ConfigMap存储普通配置，如同公开的修炼心法；
                Secret加密存储敏感信息，如同宗门的不传之秘�?
                善用此术，可使你的应用如臂使指，灵活多变�?
                现在，用你学到的配置之术，优化我们的防御系统�?
                """,
                kubernetes_concepts=["ConfigMap", "Secret", "配置管理", "环境变量"],
                commands_to_learn=["kubectl create configmap", "kubectl create secret", "kubectl get configmaps", "kubectl get secrets", "kubectl describe configmap"],
                challenge_id="chapter_3_challenge",
                reward_exp=400,
                characters=[self.characters["掌门真人"]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    __   __  ______  ______  __   __  ______  ______   �?
                �?   /\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\/\  __ \  �?
                �?   \ \ \-.  \\  __ \/\ \ \ \ \ \'\ \ \  __\\ \  __ \ �?
                �?    \ \_\\"\_\\ \____\\ \____\\ \___\_\ \_____\ \_____\�?
                �?     \/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/\/_____/�?
                �?                                                        �?
                �?    __   __  ______  ______  __   __  ______  ______   �?
                �?   /\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\/\  __ \  �?
                �?   \ \ \-.  \\  __ \/\ \ \ \ \ \'\ \ \  __\\ \  __ \ �?
                �?    \ \_\\"\_\\ \____\\ \____\\ \___\_\ \_____\ \_____\�?
                �?     \/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/\/_____/�?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \_\ \ \_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/ \/_/ \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第四�? StoryChapter(
                chapter_id=Chapter.第四�?
                title="存储之道",
                introduction="数据乃重中之重，你需要掌握数据持久化之术�?,
                narrative="""
                这一日，你发现一个严重的问题：容器重启后，之前存储的重要数据荡然无存�?
                你急忙前往藏经阁，向三师姐林雨萱请教�?

                三师姐带你来到藏经阁的深处，指着一排排古老的书架说：
                "这便�?PersistentVolume'之术，数据如同宗门典籍，需永久保存，不可或缺�?
                容器就像是临时的修炼场所，而PersistentVolume则是永久的藏经阁�?

                三师姐抽出一本古老的典籍，上面记载着存储之术�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   持久存储心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl get pv                                         �?
                �? （查看永久卷的状态）                                    �?
                �?                                                        �?
                �? kubectl get pvc                                        �?
                �? （查看永久卷声明�?                                     �?
                �?                                                        �?
                �? kubectl apply -f pvc.yaml                              �?
                �? （申请存储空间，如申请洞府一般）                         �?
                └─────────────────────────────────────────────────────────�?

                "PV是宗门提供的存储资源，如同藏经阁的书架；
                PVC是弟子对存储的申请，如同你向宗门申请的私人书架�?
                有了此术，你的应用便拥有�?记忆'，不再担心数据丢失�?
                """,
                kubernetes_concepts=["PersistentVolume", "PersistentVolumeClaim", "存储�?, "数据持久�?],
                commands_to_learn=["kubectl get pv", "kubectl get pvc", "kubectl apply", "kubectl delete pvc", "kubectl get storageclasses"],
                challenge_id="chapter_4_challenge",
                reward_exp=450,
                characters=[self.characters["三师�?]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ________  ________  ________  ________  ________     �?
                �?   /\  ____ \/\  ____ \/\  ____ \/\  ____ \/\  ____ \    �?
                �?   \ \  __\/\ \  __\/\ \  __\/\ \  __\/\ \  __\/     �?
                �?    \ \_____\/\ \_____\/\_____\/\_____\/\_____\      �?
                �?     \/_____/ \/_____\/\/_____\/\/_____\/\/_____/       �?
                �?                                                        �?
                �?    ________  ________  ________  ________  ________     �?
                �?   /\  ____ \/\  ____ \/\  ____ \/\  ____ \/\  ____ \    �?
                �?   \ \  __\/\ \  __\/\ \  __\/\ \  __\/\ \  __\/     �?
                �?    \ \_____\/\ \_____\/\_____\/\_____\/\_____\      �?
                �?     \/_____/ \/_____\/\/_____\/\/_____\/\/_____/       �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第五�? StoryChapter(
                chapter_id=Chapter.第五�?
                title="调度之学",
                introduction="成为真正的将帅，你需要掌握资源调度与分配之术�?,
                narrative="""
                随着修为提升，你被任命为一方小统领，负责管理宗门的部分资源�?
                如何合理分配资源，成为你面临的新挑战�?

                这一日，宗门的军师前来指导你�?
                "小统领，要成为一名优秀的将帅，不仅要能指挥军队�?
                更要懂得如何合理分配资源。我来传授你'资源调度'之术�?

                军师取出一张地图，上面标记着宗门的各种资源：

                ┌─────────────────────────────────────────────────────────�?
                �?                   资源调度心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl top pods                                       �?
                �? （查看各弟子的灵力消耗）                                �?
                �?                                                        �?
                �? kubectl describe node master                           �?
                �? （查看节点资源，如查看灵山灵脉）                        �?
                �?                                                        �?
                �? kubectl label node worker-1 node-role.kubernetes.io/   �?
                �? worker=                                               �?
                �? （标记节点，如划分修炼区域）                            �?
                └─────────────────────────────────────────────────────────�?

                "善用此术，可使宗门资源得到最优分配，
                让每位弟子都能各司其职，发挥最大潜力�?
                现在，用你学到的调度之术，优化宗门的资源分配�?
                """,
                kubernetes_concepts=["资源管理", "节点调度", "Labels", "Taints和Tolerations"],
                commands_to_learn=["kubectl top", "kubectl describe node", "kubectl label node", "kubectl get nodes", "kubectl cordon node", "kubectl uncordon node"],
                challenge_id="chapter_5_challenge",
                reward_exp=500,
                characters=[self.characters["神秘�?]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    ______  __   __  ______  ______  __   __  ______     �?
                �?   /\  ___\/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\    �?
                �?   \ \  __\ \ \-.  \  __ \/\ \ \ \ \ \'\ \ \  __\     �?
                �?    \ \_____\ \_\\"\_\ \____\\ \____\\ \___\_\ \_____\  �?
                �?     \/_____/\/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/  �?
                �?                                                        �?
                �?    ______  __   __  ______  ______  __   __  ______     �?
                �?   /\  ___\/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\    �?
                �?   \ \  __\ \ \-.  \  __ \/\ \ \ \ \ \'\ \ \  __\     �?
                �?    \ \_____\ \_\\"\_\ \____\\ \____\\ \___\_\ \_____\  �?
                �?     \/_____/\/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/  �?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第六�? StoryChapter(
                chapter_id=Chapter.第六�?
                title="故障排查",
                introduction="在危机中救火，是每个强者必备的技能�?,
                narrative="""
                这一日，宗门突然陷入混乱�?报——！核心服务全部瘫痪�?
                魔教正在趁机进攻�?

                你临危受命，负责排查故障。这是一次考验，也是成长的机会�?
                掌门真人远程传声指导�?

                "徒儿，现在是考验你的时候了。记住，排查故障如同寻医问诊�?
                需望闻问切，循序渐进。先看日志，再看事件，最后亲自探查�?

                掌门真人的声音刚落，你的脑海中便浮现出故障排查的心法�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   故障排查心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl logs deployment/web --tail=100                 �?
                �? （查看最近的战斗记录�?                                 �?
                �?                                                        �?
                �? kubectl exec -it <pod-name> -- /bin/sh                �?
                �? （进入容器内部，如亲临战场）                            �?
                �?                                                        �?
                �? kubectl port-forward svc/web 8080:80                  �?
                �? （建立秘密通道，远程诊断）                              �?
                �?                                                        �?
                �? kubectl events --sort-by='.lastTimestamp'             �?
                �? （查看最近的天机变化�?                                 �?
                └─────────────────────────────────────────────────────────�?

                "去吧，用你学到的故障排查之术，拯救宗门于危难之中�?
                """,
                kubernetes_concepts=["日志查看", "Pod调试", "端口转发", "事件监控"],
                commands_to_learn=["kubectl logs", "kubectl exec", "kubectl port-forward", "kubectl events", "kubectl debug"],
                challenge_id="chapter_6_challenge",
                reward_exp=550,
                characters=[self.characters["掌门真人"]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  __   __  ______  ______  __   __  ______     �?
                �?   /\  ___\/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\    �?
                �?   \ \  __\ \ \-.  \  __ \/\ \ \ \ \ \'\ \ \  __\     �?
                �?    \ \_____\ \_\\"\_\ \____\\ \____\\ \___\_\ \_____\  �?
                �?     \/_____/\/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/  �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第七�? StoryChapter(
                chapter_id=Chapter.第七�?
                title="进阶操作",
                introduction="你已经掌握基础，是时候学习更高深的学问�?,
                narrative="""
                魔教教主血魔亲自来袭，宗门陷入前所未有的危机�?
                掌门真人将你叫到跟前�?
                "徒儿，现在是生死存亡之际。我将传授你最后的进阶秘术�?
                希望你能凭借此术，拯救宗门�?

                掌门真人双手结印，空中出现了进阶秘术的心法：

                ┌─────────────────────────────────────────────────────────�?
                �?                   进阶秘术                             �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl apply -f deployment.yaml                       �?
                �? （以不变应万变，批量操作�?                             �?
                �?                                                        �?
                �? kubectl patch deployment web -p \                      �?
                �?     '{\"spec\":{\"replicas\":5}}'                          �?
                �? （以巧破力，局部更新）                                  �?
                �?                                                        �?
                �? kubectl set image deployment/web \                    �?
                �?     nginx=nginx:1.21                                   �?
                �? （改天换日，更新镜像�?                                 �?
                �?                                                        �?
                �? kubectl rollout undo deployment/web                    �?
                �? （时光倒流，回滚版本）                                  �?
                └─────────────────────────────────────────────────────────�?

                "此乃YAML之道，可批量、可更新、可回滚�?
                掌握此术，你便可以一敌万，以一当十�?
                现在，用你学到的进阶之术，对抗血魔！"
                """,
                kubernetes_concepts=["YAML配置", "批量操作", "补丁更新", "版本回滚"],
                commands_to_learn=["kubectl apply", "kubectl patch", "kubectl set image", "kubectl rollout undo", "kubectl rollout history"],
                challenge_id="chapter_7_challenge",
                reward_exp=600,
                characters=[self.characters["掌门真人"], self.characters["魔教教主"]],
                events=[],
                boss_fight=True,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    ______  __   __  ______  ______  __   __  ______     �?
                �?   /\  ___\/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\    �?
                �?   \ \  __\ \ \-.  \  __ \/\ \ \ \ \ \'\ \ \  __\     �?
                �?    \ \_"\_\ \____\ \____\ \___\_\ \_____\ \_____\  �?
                �?     \/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  __   __  ______  ______  __   __  ______     �?
                �?   /\  ___\/\ "-.\ \  __ \/\  __ \/\ \ /\ \/\  ___\    �?
                �?   \ \  __\ \ \-.  \  __ \/\ \ \ \ \ \'\ \ \  __\     �?
                �?    \ \_"\_\ \____\ \____\ \___\_\ \_____\ \_____\  �?
                �?     \/_/ \/_/ \/_____\/_____/\/___/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \___\/\_____\/\_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/   \/_____/\/_/\/_/ \/_____/\/_____/  �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第八�? StoryChapter(
                chapter_id=Chapter.第八�?
                title="网络与安�?,
                introduction="在修真界，网络与安全是守护宗门的最后防线�?,
                narrative="""
                血魔被你击败，但宗门的防御体系也受到了重创�?
                大师兄李青峰找到你：
                "小师弟，这次危机让我们意识到，宗门的网络与安全体系还不够完善�?
                我来传授�?网络与安�?之术，这是守护宗门的最后防线�?

                大师兄取出一面盾牌和一把剑�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   网络安全心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl get networkpolicies                            �?
                �? （查看网络策略，如查看宗门的防御阵法�?                 �?
                �?                                                        �?
                �? kubectl get roles                                      �?
                �? （查看角色权限，如查看宗门弟子的身份令牌�?             �?
                �?                                                        �?
                �? kubectl auth can-i create pods                         �?
                �? （验证权限，如确认弟子资格）                            �?
                └─────────────────────────────────────────────────────────�?

                "网络策略如同宗门的防御阵法，保护内部网络不受外敌入侵�?
                权限管理如同宗门的身份令牌，确保只有授权弟子才能访问敏感资源�?
                善用此术，可使宗门固若金汤，万无一失�?
                """,
                kubernetes_concepts=["网络策略", "RBAC权限", "Secret管理", "安全最佳实�?],
                commands_to_learn=["kubectl get networkpolicies", "kubectl get roles", "kubectl get rolebindings", "kubectl auth can-i"],
                challenge_id="chapter_8_challenge",
                reward_exp=650,
                characters=[self.characters["大师�?]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────�?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    �?
                �?   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \   �?
                �?    \ \_____\/\ \_\ \ \_\/\_\/\_____\/\_____\  �?
                �?     \/_____/\/_/ _/ \/_____/\/_/_/ \/_____/\/_____/  �?
                �?                                                        �?
                �?    ______  ______  ______  ______  ______  ______     �?
                �?   / __  __  __  __  __  __    �?
                �?    __  __  __  __  __   �?
                �?    __________________ �?
                �?     _____/_/   _____/_/_/ _____/_____/  �?
                �?                                                        �?
                �?    ________  ________  ________  ________  ________     �?
                �?   / ____  ____  ____  ____  ____    �?
                �?    __ __ __ __ __     �?
                �?    ____________________     �?
                �?     _____/ \/____________________/       �?
                �?                                                        �?
                └─────────────────────────────────────────────────────────�?
                """
            ),

            Chapter.第九�? StoryChapter(
                chapter_id=Chapter.第九�?
                title="集群管理",
                introduction="掌握集群管理之术，成为真正的宗门领袖�?,
                narrative="""
                经过一系列的战斗和修炼，你已经成长为宗门的核心弟子�?
                掌门真人决定传授你集群管理之术，让你成为真正的宗门领袖：

                "徒儿，你已经掌握了各种容器化之术，现在是时候学习如何管理整个集群了�?
                集群管理之术是修真界的最高奥秘，掌握此术，你便可以俯瞰整个修真界�?

                掌门真人手指向天，整个修真界的地图浮现在空中�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   集群管理心法                          �?
                ├─────────────────────────────────────────────────────────�?
                �? kubectl cluster-info                                   �?
                �? （查看集群信息，如俯瞰整个修真界�?                     �?
                �?                                                        �?
                �? kubectl api-resources                                  �?
                �? （查看所有API资源，如阅览藏经阁）                       �?
                �?                                                        �?
                �? kubectl config view                                    �?
                �? （查看配置文件，如查看宗门规矩）                        �?
                �?                                                        �?
                �? kubectl version                                        �?
                �? （查看版本信息，如查看修为境界）                        �?
                └─────────────────────────────────────────────────────────�?

                "集群管理之术是连接天地的桥梁，通过它你可以掌控整个集群的命运�?
                现在，用你学到的集群管理之术，带领宗门走向辉煌！"
                """,
                kubernetes_concepts=["集群管理", "API资源", "配置管理", "版本控制"],
                commands_to_learn=[
                    "kubectl cluster-info",
                    "kubectl api-resources",
                    "kubectl config view",
                    "kubectl version"
                ],
                challenge_id="chapter_9_challenge",
                reward_exp=700,
                characters=[self.characters["掌门真人"]],
                events=[],
                boss_fight=False
            ),

            Chapter.第十�? StoryChapter(
                chapter_id=Chapter.第十�?
                title="云厂商管�?,
                introduction="掌握云厂商的Kubernetes管理之道，成为跨云时代的强者�?,
                narrative="""
                魔教之乱平定后，修真界进入了跨云时代。各大门派纷纷与云厂商合作，
                建立了更强大的集群体系。你作为青云宗的新任掌门，需要掌握云厂商的管理之术�?

                这一日，四位神秘使者来到宗门，他们分别来自四大云厂商：
                "阿里云使�?�?腾讯云使�?�?华为云使�?�?火山引擎使�?�?

                阿里云使者上前说道："掌门，我们带来了云厂商的Kubernetes管理心法�?
                掌握此术，可让你在跨云时代如鱼得水�?

                四位使者合力展示了云厂商心法：

                ┌─────────────────────────────────────────────────────────�?
                �?                   云厂商管理心�?                         �?
                ├─────────────────────────────────────────────────────────�?
                �? aliyun ack list-clusters                               �?
                �? （查看阿里云ACK集群，如查看宗门分舵�?                   �?
                �?                                                        �?
                �? tkecluster list                                        �?
                �? （查看腾讯云TKE集群，如查看友邻门派�?                   �?
                �?                                                        �?
                �? cce cluster list                                       �?
                �? （查看华为云CCE集群，如查看同盟势力�?                   �?
                �?                                                        �?
                �? vke cluster list                                       �?
                �? （查看火山引擎VKE集群，如查看新兴势力�?                 �?
                └─────────────────────────────────────────────────────────�?

                "云厂商的Kubernetes服务各有特色，但核心原理相通�?
                掌握这些心法，你便可以管理不同云厂商的集群，
                在跨云时代建立自己的势力范围�?
                """,
                kubernetes_concepts=["云厂商Kubernetes服务", "跨云管理", "集群生命周期"],
                commands_to_learn=[
                    "aliyun ack list-clusters",
                    "tkecluster list",
                    "cce cluster list",
                    "vke cluster list"
                ],
                challenge_id="chapter_10_challenge",
                reward_exp=750,
                characters=[self.characters["掌门真人"], self.characters["神秘�?]],
                events=[],
                boss_fight=False
            ),

            Chapter.第十一�? StoryChapter(
                chapter_id=Chapter.第十一�?
                title="云厂商高级特�?,
                introduction="探索云厂商的高级特性，让你的集群更加强大�?,
                narrative="""
                你已经掌握了云厂商集群的基本管理，但云厂商的高级特性才是真正的宝库�?
                这一日，四位使者再次来访，带来了更高级的心法：

                "掌门，云厂商提供了许多高级特性，可以让你的集群更加强大�?
                今天我们将传授你这些高级心法�?

                使者们展示了高级心法：

                ┌─────────────────────────────────────────────────────────�?
                �?                   云厂商高级心�?                         �?
                ├─────────────────────────────────────────────────────────�?
                �? aliyun ack add-node --cluster-id CLUSTER_ID            �?
                �? （为ACK集群添加节点，如招收新弟子）                    �?
                �?                                                        �?
                �? tke node create --cluster-id CLUSTER_ID                �?
                �? （为TKE集群添加节点，如扩充门派势力�?                   �?
                �?                                                        �?
                �? cce node create --cluster-id CLUSTER_ID                �?
                �? （为CCE集群添加节点，如壮大同盟�?                     �?
                �?                                                        �?
                �? vke node-pool create --cluster-id CLUSTER_ID           �?
                �? （为VKE集群创建节点池，如建立分舵）                    �?
                └─────────────────────────────────────────────────────────�?

                "这些高级特性可以帮助你更好地管理集群资源，
                应对各种复杂场景。善用这些特性，
                你的集群将无坚不摧，在跨云时代立于不败之地！"
                """,
                kubernetes_concepts=["节点管理", "节点�?, "集群扩展", "云厂商特�?],
                commands_to_learn=["aliyun ack add-node", "tke node create", "cce node create", "vke node-pool create"],
                challenge_id="chapter_11_challenge",
                reward_exp=800,
                characters=[self.characters["掌门真人"], self.characters["大师�?], self.characters["二师�?]],
                events=[],
                boss_fight=False
            ),

            Chapter.终章: StoryChapter(
                chapter_id=Chapter.终章,
                title="飞升大成",
                introduction="历经磨难，你终于悟道飞升，成为一代宗师�?,
                narrative="""
                魔教教主血魔被你彻底击败，你名声大噪，成为修真界新一代传奇�?
                宗门举行了盛大的庆典，庆祝你的胜利�?

                掌门真人欣慰地看着你："徒儿，你已掌握容器化之道的精髓，
                成为了一代宗师。今日本座宣布，你正式成为青云宗的新一代掌门！"

                众弟子齐声欢呼，你站在云端，俯瞰整个修真界，心中一片澄明�?

                ┌─────────────────────────────────────────────────────────�?
                �?                   宗师心法                             �?
                ├─────────────────────────────────────────────────────────�?
                �? 容器之道，在于平衡与和谐                               �?
                �? 集群管理，在于统筹与调度                               �?
                �? 网络安全，在于防御与监控                               �?
                �? 进阶操作，在于灵活与变�?                              �?
                �? 云厂商管理，在于跨云协同                               �?
                └─────────────────────────────────────────────────────────�?

                "记住，技术之路，永无止境。容器之道，亦是人生之道—�?
                在于平衡，在于和谐，在于将复杂之事化于简单之间�?
                现在，你已经掌握了Kubernetes之道的精髓，
                可以随心所欲地操控各种资源，创造属于你的传奇！"

                你抬头望向更高的天空，心中充满了无限的可能�?
                凡人之躯，终可问道苍穹�?

                ╔═══════════════════════════════════════════════════════�?
                �?          🎉 恭喜你已飞升大成�?🎉                      �?
                �?                                                          �?
                �?      你已掌握Kubernetes之道的精髓，成为一代宗师！        �?
                �?                                                          �?
                �?      愿你将此道发扬光大，守护世间的和平与秩序�?         �?
                ╚═══════════════════════════════════════════════════════�?
                """,
                kubernetes_concepts=["Kubernetes全貌", "最佳实�?, "持续学习", "跨云管理"],
                commands_to_learn=["kubectl completion", "kubectl plugin list"],
                challenge_id="final_challenge",
                reward_exp=1000,
                characters=[self.characters["掌门真人"], self.characters["大师�?], self.characters["二师�?], self.characters["三师�?], self.characters["四师�?]],
                events=[],
                boss_fight=False
            ),
        }

    def get_current_chapter(self) -> StoryChapter:
        """获取当前章节

        Returns:
            StoryChapter: 当前章节对象
        """
        return self.chapters[self.current_chapter]

    def get_chapter(self, chapter: Chapter) -> Optional[StoryChapter]:
        """获取指定章节

        Args:
            chapter: 章节ID

        Returns:
            Optional[StoryChapter]: 指定章节对象，如果不存在则返回None
        """
        return self.chapters.get(chapter)

    def advance_chapter(self) -> bool:
        """推进到下一�?

        Returns:
            bool: 如果成功推进到下一章节则返回True，否则返回False
        """
        chapter_order = list(Chapter)
        current_index = chapter_order.index(self.current_chapter)

        if current_index < len(chapter_order) - 1:
            self.current_chapter = chapter_order[current_index + 1]
            return True
        return False

    def get_all_commands(self) -> List[str]:
        """获取所有命�?

        Returns:
            List[str]: 所有章节的命令列表
        """
        commands = []
        for chapter in self.chapters.values():
            commands.extend(chapter.commands_to_learn)
        return commands

    def get_chapter_commands(self, chapter: Chapter) -> List[str]:
        """获取指定章节的命�?

        Args:
            chapter: 章节ID

        Returns:
            List[str]: 指定章节的命令列�?
        """
        chapter_obj = self.get_chapter(chapter)
        if chapter_obj:
            return chapter_obj.commands_to_learn
        return []

    def get_total_chapters(self) -> int:
        """获取总章节数

        Returns:
            int: 总章节数
        """
        return len(self.chapters)

    def get_completed_chapters(self, player: Player) -> int:
        """获取已完成章节数

        Args:
            player: 玩家对象

        Returns:
            int: 已完成章节数
        """
        completed = 0
        chapter_challenge_map = {
            Chapter.序章: "prologue_challenge",
            Chapter.第一�? "chapter_1_challenge",
            Chapter.第二�? "chapter_2_challenge",
            Chapter.第三�? "chapter_3_challenge",
            Chapter.第四�? "chapter_4_challenge",
            Chapter.第五�? "chapter_5_challenge",
            Chapter.第六�? "chapter_6_challenge",
            Chapter.第七�? "chapter_7_challenge",
            Chapter.第八�? "chapter_8_challenge",
            Chapter.第九�? "chapter_9_challenge",
            Chapter.终章: "final_challenge"
        }

        for chapter, challenge_id in chapter_challenge_map.items():
            if challenge_id in player.challenges_completed:
                completed += 1
        return completed

    def get_story_progress(self, player: Player) -> Dict[str, Any]:
        """获取故事进度

        Args:
            player: 玩家对象

        Returns:
            Dict[str, Any]: 故事进度字典
        """
        return {
            "current_chapter": self.current_chapter.value,
            "current_title": self.get_current_chapter().title,
            "total_chapters": self.get_total_chapters(),
            "completed_chapters": self.get_completed_chapters(player),
            "all_commands": len(self.get_all_commands()),
            "mastered_commands": len(player.kubectl_commands_mastered),
            "current_chapter_commands": len(self.get_current_chapter().commands_to_learn),
            "current_chapter_concepts": self.get_current_chapter().kubernetes_concepts
        }

    def get_random_event(self, player_level: int) -> Optional[StoryEvent]:
        """获取随机事件

        根据玩家等级，随机返回一个适合的事件�?

        Args:
            player_level: 玩家等级

        Returns:
            Optional[StoryEvent]: 随机事件对象，如果没有适合的事件则返回None
        """
        available_events = [event for event in self.random_events if event.required_level <= player_level]
        if available_events:
            return random.choice(available_events)
        return None

    def get_chapter_characters(self, chapter: Chapter) -> List[Character]:
        """获取指定章节的人物列�?

        Args:
            chapter: 章节ID

        Returns:
            List[Character]: 章节人物列表
        """
        chapter_obj = self.get_chapter(chapter)
        if chapter_obj:
            return chapter_obj.characters
        return []

    def is_boss_chapter(self, chapter: Chapter) -> bool:
        """检查章节是否有boss�?

        Args:
            chapter: 章节ID

        Returns:
            bool: 如果章节有boss战则返回True，否则返回False
        """
        chapter_obj = self.get_chapter(chapter)
        if chapter_obj:
            return chapter_obj.boss_fight
        return False

