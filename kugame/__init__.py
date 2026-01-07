"""KuGame - 游戏化学习Kubernetes的命令行工具

通过武侠故事的方式，让学习Kubernetes命令变得有趣且富有挑战性。
"""

__version__ = "1.0.0"
__author__ = "KuGame Team"

from .player import Player
from .game_engine import GameEngine
from .story import StoryManager
from .kubernetes_commands import KubernetesCommandManager

__all__ = [
    "__version__",
    "Player",
    "GameEngine",
    "StoryManager",
    "KubernetesCommandManager",
]
