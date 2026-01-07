"""命令行界面

KuGame的交互式命令行界面。
"""

import sys
import os
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.style import Style
from rich.color import Color
from rich import box
from .game_engine import GameEngine, GameState
from .player import Sect
from .story import Chapter


class CLI:
    """命令行界面"""
    
    def __init__(self) -> None:
        self.console = Console()
        self.engine = GameEngine()
        self.running = True
    
    def clear_screen(self) -> None:
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self) -> None:
        """打印游戏横幅"""
        banner = """
        ╔═══════════════════════════════════════════════════════════════════╗
        ║                                                                   ║
        ║      ████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗                   ║
        ║      ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝                   ║
        ║         ██║   ███████║███████║██║     █████╔╝                    ║
        ║         ██║   ██╔══██║██╔══██║██║     ██╔═██╗                    ║
        ║         ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗                   ║
        ║         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                   ║
        ║                                                                   ║
        ║              游戏化学习 Kubernetes 命令行工具                     ║
        ║                                                                   ║
        ╚═══════════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold magenta")
        self.console.print()
    
    def print_menu(self, options: List[Dict[str, str]]) -> None:
        """打印菜单"""
        table = Table(box=box.ROUNDED, show_header=False)
        table.add_column("选项", justify="right", style="cyan")
        table.add_column("名称", style="green")
        table.add_column("描述", style="white")
        
        for idx, option in enumerate(options, 1):
            table.add_row(
                f"[{idx}]",
                option["name"],
                option["description"]
            )
        
        self.console.print(Panel(table, title="主菜单", border_style="blue"))
    
    def get_sect_selection(self) -> Sect:
        """获取门派选择"""
        self.console.print("\n[bold yellow]选择你的门派：[/bold yellow]\n")
        
        sects = list(Sect)
        for idx, sect in enumerate(sects, 1):
            self.console.print(f"[{idx}] {sect.value}")
        
        self.console.print()
        choice = Prompt.ask("请输入门派编号", default="1")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sects):
                return sects[idx]
        except ValueError:
            pass
        
        return Sect.青云宗
    
    def start(self) -> None:
        """开始游戏"""
        self.clear_screen()
        self.print_banner()
        
        if self.engine.load_player():
            player = self.engine.player
            if player:
                self.console.print(f"[green]✓ 欢迎回来，[/green][cyan]{player.title}[/cyan]！")
                self.console.print()
        else:
            self.console.print("[bold yellow]新侠客，欢迎来到KuGame！[/bold yellow]\n")
            name = Prompt.ask("请输入你的侠名", default="无名")
            sect = self.get_sect_selection()
            self.engine.initialize_player(name, sect)
            player = self.engine.player
            if player:
                self.console.print(f"\n[green]✓ 欢迎加入[/green][cyan]{sect.value}[/cyan]，{player.title}侠客！")
        
        self.main_loop()
    
    def main_loop(self) -> None:
        """主循环"""
        while self.running:
            self.console.print()
            self.console.print("[bold magenta]─" * 60)
            self.console.print("[bold magenta]│  🏔️  Kubernetes 修仙之旅 🏔️  │")
            self.console.print("[bold magenta]─" * 60)
            self.console.print()
            
            options = self.engine.get_menu_options()
            self.print_menu(options)
            
            self.console.print()
            choice = Prompt.ask("[bold yellow]请选择你的行动：[/bold yellow]", default="1")
            
            self.handle_choice(choice)
    
    def handle_choice(self, choice: str) -> None:
        """处理用户选择
        
        Args:
            choice: 用户选择的选项
        """
        options = {f"{idx}": opt["id"] for idx, opt in enumerate(self.engine.get_menu_options(), 1)}
        
        action = options.get(choice)
        
        if action == "story":
            self.play_story()
        elif action == "practice":
            self.practice()
        elif action == "challenge":
            self.do_challenge()
        elif action == "quiz":
            self.do_quiz()
        elif action == "progress":
            self.show_progress()
        elif action == "commands":
            self.show_commands()
        elif action == "save":
            self.save_game()
        elif action == "save_manager":
            self.manage_saves()
        elif action == "quit":
            self.quit_game()
        else:
            self.console.print("[red]无效选择，请重新输入[/red]")
    
    def play_story(self) -> None:
        """播放故事"""
        self.clear_screen()
        story = self.engine.get_story_content()
        
        # 增加故事播放的沉浸式效果
        self.console.print("[bold magenta]" + "═" * 70)
        self.console.print(f"[bold magenta]│{('第' + story['chapter_id'] + '章 - ' + story['title']).center(68)}│")
        self.console.print("[bold magenta]" + "═" * 70)
        self.console.print()
        
        # 显示故事介绍，增加神秘感
        self.console.print(Panel(
            "[italic]" + story["introduction"] + "[/italic]",
            border_style="cyan",
            box=box.DOUBLE_EDGE
        ))
        self.console.print()
        
        # 故事背景展示
        self.console.print("[bold yellow]🌟 故事背景 🌟[/bold yellow]")
        self.console.print("[dim cyan]" + "─" * 60 + "[/dim cyan]")
        self.console.print(story["narrative"])
        self.console.print()
        
        # 本章节学习内容
        if story["commands"]:
            self.console.print("[bold green]📜 本章节修炼内容 📜[/bold green]")
            self.console.print("[dim cyan]" + "─" * 60 + "[/dim cyan]")
            for idx, cmd in enumerate(story["commands"], 1):
                self.console.print(f"  [{idx}] {cmd}")
            
            self.console.print()
            self.console.print("[bold cyan]🎁 完成奖励 🎁[/bold cyan]")
            self.console.print(f"  • 经验值：[green]{story['reward_exp']}[/green]")
            self.console.print(f"  • 境界提升：[yellow]有可能突破当前境界[/yellow]")
        
        self.console.print()
        self.console.print("[dim cyan]" + "─" * 70 + "[/dim cyan]")
        
        # 增加更有故事性的提示
        if story["commands"]:
            if Confirm.ask("\n[bold magenta]是否准备好迎接挑战，开始修炼？[/bold magenta]"):
                self.do_challenge()
        else:
            if Confirm.ask("\n[bold magenta]是否准备好继续修炼之旅？[/bold magenta]"):
                self.advance_story()
    
    def practice(self) -> None:
        """练习模式"""
        self.clear_screen()
        commands = self.engine.get_practice_commands()
        
        if not commands:
            self.console.print("[yellow]还没有掌握任何命令，请先完成故事章节[/yellow]")
            return
        
        self.console.print(f"[bold]已掌握 {len(commands)} 个命令[/bold]\n")
        
        for idx, cmd in enumerate(commands, 1):
            self.console.print(f"[{idx}] {cmd}")
        
        self.console.print("\n输入命令编号进行练习，输入'q'返回菜单")
        
        while True:
            choice = Prompt.ask("命令编号")
            
            if choice.lower() == 'q':
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(commands):
                    self.show_command_practice(commands[idx])
            except ValueError:
                self.console.print("[red]无效输入[/red]")
    
    def show_command_practice(self, command: str) -> None:
        """显示命令练习"""
        cmd_info = self.engine.command_manager.get_command(command)
        
        if not cmd_info:
            return
        
        panel = Panel(
            f"[bold]命令：[/bold]{command}\n\n"
            f"[bold]语法：[/bold]{cmd_info.syntax}\n\n"
            f"[bold]示例：[/bold]\n{cmd_info.example}\n\n"
            f"[bold]说明：[/bold]{cmd_info.description}\n\n"
            f"[bold]相关概念：[/bold]{cmd_info.kubernetes_concept}",
            title=f"练习：{command}",
            border_style="green"
        )
        
        self.console.print(panel)
    
    def do_challenge(self) -> None:
        """执行挑战"""
        self.clear_screen()
        challenge = self.engine.generate_challenge()
        
        if not challenge:
            self.console.print("[yellow]暂无可用挑战[/yellow]")
            return
        
        # 构建挑战面板内容，包含选项
        challenge_content = f"[bold]挑战：{challenge.title}[/bold]\n\n"
        challenge_content += f"{challenge.description}\n\n"
        challenge_content += f"[bold]问题：[/bold]{challenge.question}\n\n"
        
        # 添加选项
        challenge_content += "[bold]选项：[/bold]\n"
        for idx, option in enumerate(challenge.options, 1):
            challenge_content += f"  [{idx}] {option}\n"
        
        challenge_content += f"\n[italic]提示：{challenge.hint}[/italic]"
        
        self.console.print(Panel(
            challenge_content,
            title="⚔️ 挑战任务",
            border_style="red"
        ))
        
        # 获取用户选择
        while True:
            try:
                user_input = Prompt.ask("\n请选择你的答案 (1-4)")
                user_choice = int(user_input)
                if 1 <= user_choice <= len(challenge.options):
                    break
                else:
                    self.console.print(f"[red]无效选择，请输入1-{len(challenge.options)}之间的数字[/red]")
            except ValueError:
                self.console.print("[red]无效输入，请输入数字[/red]")
        
        result = self.engine.check_answer(user_choice)
        
        self.console.print()
        if result["correct"]:
            self.console.print(Panel(
                f"[bold green]{result['message']}[/bold green]\n\n"
                f"当前连击：{result['streak']}\n"
                f"总得分：{result['score']}",
                title="✓ 挑战成功",
                border_style="green"
            ))
            
            if Confirm.ask("\n是否继续下一章？"):
                self.advance_story()
        else:
            self.console.print(Panel(
                f"[bold red]{result['message']}[/bold red]\n\n"
                f"[yellow]提示：{result.get('hint', '')}[/yellow]",
                title="✗ 挑战失败",
                border_style="red"
            ))
            self.engine.reset_streak()
    
    def advance_story(self) -> None:
        """推进故事"""
        if self.engine.advance_chapter():
            self.engine.save_game()
            self.console.print("[bold green]✓ 成功进入下一章节！[/bold green]")
        else:
            self.console.print("[bold yellow]已是最终章节，恭喜你完成全部挑战！[/bold yellow]")
    
    def do_combat(self, monster: Any) -> None:
        """执行战斗
        
        Args:
            monster: 要战斗的怪物对象
        """
        self.clear_screen()
        
        # 开始战斗
        combat_state = self.engine.start_combat(monster)
        
        self.console.print(Panel(
            f"[bold red]{monster.name}出现了！[/bold red]\n\n" \
            f"{monster.description}\n\n" \
            f"[bold]怪物属性：[/bold]\n" \
            f"生命值：{monster.health} | 攻击力：{monster.attack} | 防御力：{monster.defense}\n\n" \
            f"[bold]击败奖励：[/bold]{monster.experience_reward} 经验值",
            title="⚔️ 战斗开始",
            border_style="red"
        ))
        
        # 战斗循环
        player = self.engine.player
        if not player:
            self.console.print("[red]错误：玩家未初始化，无法进行战斗！[/red]")
            return
            
        while True:
            # 显示战斗状态
            self.console.print("\n[bold]当前战斗状态：[/bold]")
            self.console.print(f"[green]你的生命值：{player.health}/{player.max_health}[/green]")
            self.console.print(f"[red]{monster.name}的生命值：{self.engine.monster_current_health}/{monster.health}[/red]")
            self.console.print()
            
            # 显示战斗选项
            combat_options = [
                {"id": "attack", "name": "攻击", "description": "回答命令题，对怪物造成伤害"},
                {"id": "flee", "name": "逃跑", "description": "尝试逃离战斗（成功率50%）"}
            ]
            
            table = Table(box=box.ROUNDED, show_header=False)
            table.add_column("选项", justify="right", style="cyan")
            table.add_column("名称", style="green")
            table.add_column("描述", style="white")
            
            for idx, option in enumerate(combat_options, 1):
                table.add_row(
                    f"[{idx}]",
                    option["name"],
                    option["description"]
                )
            
            self.console.print(Panel(table, title="战斗选项", border_style="red"))
            
            # 获取玩家选择
            choice = Prompt.ask("\n请选择战斗行动", default="1")
            
            try:
                action_idx = int(choice) - 1
                if 0 <= action_idx < len(combat_options):
                    action = combat_options[action_idx]["id"]
                    
                    if action == "attack":
                        # 生成命令挑战
                        challenge = self.engine.generate_challenge()
                        
                        if not challenge:
                            self.console.print("[yellow]暂无可用挑战，战斗结束[/yellow]")
                            return
                        
                        # 显示挑战问题
                        self.console.print("\n")
                        self.console.print(Panel(
                            f"[bold]挑战：{challenge.title}[/bold]\n\n" \
                            f"{challenge.description}\n\n" \
                            f"[bold]问题：[/bold]{challenge.question}\n\n" \
                            f"[bold]选项：[/bold]\n" \
                            + "\n".join([f"  [{idx+1}] {option}" for idx, option in enumerate(challenge.options)]),
                            title="💡 命令挑战",
                            border_style="blue"
                        ))
                        
                        # 获取答案选择
                        while True:
                            try:
                                answer_choice = int(Prompt.ask("\n请选择你的答案 (1-4)"))
                                if 1 <= answer_choice <= len(challenge.options):
                                    break
                                else:
                                    self.console.print(f"[red]无效选择，请输入1-{len(challenge.options)}之间的数字[/red]")
                            except ValueError:
                                self.console.print("[red]无效输入，请输入数字[/red]")
                        
                        # 检查答案
                        result = self.engine.check_answer(answer_choice)
                        
                        # 处理战斗结果
                        combat_result = self.engine.player_attack(monster, result["correct"])
                        
                        self.console.print("\n")
                        self.console.print(Panel(
                            f"{combat_result['message']}",
                            title="⚔️ 战斗结果",
                            border_style="green" if combat_result["status"] == "combat_won" else "red"
                        ))
                        
                        # 检查战斗是否结束
                        if combat_result["status"] == "combat_won":
                            # 战斗胜利
                            self.console.print(f"\n[bold green]✓ 战斗胜利！[/bold green]获得了{combat_result['exp_gained']}经验值！")
                            return
                        elif combat_result["status"] == "combat_lost":
                            # 战斗失败
                            self.console.print("\n[bold red]✗ 你被击败了！[/bold red]")
                            return
                        
                    elif action == "flee":
                        # 尝试逃跑
                        flee_result = self.engine.flee_combat(monster)
                        
                        self.console.print("\n")
                        self.console.print(Panel(
                            flee_result["message"],
                            title="🏃 逃跑结果",
                            border_style="yellow"
                        ))
                        
                        if flee_result["status"] == "flee_success":
                            # 逃跑成功
                            return
                    
            except ValueError:
                self.console.print("[red]无效输入[/red]")
    
    def do_quiz(self) -> None:
        """执行测验"""
        self.clear_screen()
        quiz = self.engine.generate_quiz()
        
        if not quiz or not quiz.get("question"):
            self.console.print("[yellow]请先完成一些故事章节[/yellow]")
            return
        
        self.console.print(Panel(
            quiz["question"],
            title="📝 知识问答",
            border_style="cyan"
        ))
        
        for idx, option in enumerate(quiz["options"], 1):
            self.console.print(f"[{idx}] {option}")
        
        answer = Prompt.ask("\n请选择答案")
        
        try:
            choice = int(answer) - 1
            if 0 <= choice < len(quiz["options"]):
                correct = choice == quiz["correct_index"]
                
                if correct:
                    self.console.print("[bold green]✓ 回答正确！[/bold green]")
                else:
                    self.console.print(f"[bold red]✗ 回答错误[/bold red]，正确答案是：{quiz['options'][quiz['correct_index']]}")
                
                self.console.print(f"\n[yellow]说明：{quiz['explanation']}[/yellow]")
        except ValueError:
            self.console.print("[red]无效输入[/red]")
    
    def do_pure_quiz(self) -> None:
        """执行纯粹答题模式"""
        self.clear_screen()
        
        # 选择答题模式
        mode_options = [
            {"id": "all", "name": "全部命令", "description": "从所有命令中随机出题"},
            {"id": "wrong", "name": "错题集", "description": "只从你答错的命令中出题"}
        ]
        
        self.console.print(Panel(
            "欢迎进入纯粹答题模式！\n在这里你可以反复练习Kubernetes命令，提高你的技能水平。",
            title="📚 纯粹答题模式",
            border_style="cyan"
        ))
        
        self.console.print("\n[bold yellow]选择答题模式：[/bold yellow]\n")
        
        for idx, option in enumerate(mode_options, 1):
            self.console.print(f"[{idx}] {option['name']} - {option['description']}")
        
        self.console.print()
        mode_choice = Prompt.ask("请选择模式", default="1")
        
        try:
            mode_idx = int(mode_choice) - 1
            if 0 <= mode_idx < len(mode_options):
                use_wrong_commands_only = mode_idx == 1
                
                # 开始答题模式
                quiz_state = self.engine.start_quiz_mode(use_wrong_commands_only)
                
                self.console.print(f"\n[green]已进入{quiz_state['mode']}，共有{quiz_state['total_commands']}个命令可练习[/green]")
                self.console.print("\n输入 'q' 退出答题模式\n")
                
                # 答题循环
                while True:
                    # 生成题目
                    quiz_question = self.engine.generate_quiz_question(use_wrong_commands_only)
                    
                    if not quiz_question:
                        self.console.print("\n[yellow]所有命令都已掌握，退出答题模式[/yellow]")
                        break
                    
                    # 显示题目
                    self.console.print(Panel(
                        f"[bold]问题：[/bold]{quiz_question['question']}\n\n" \
                        + "\n".join([f"  [{idx+1}] {option}" for idx, option in enumerate(quiz_question['options'])]),
                        title="📝 命令练习",
                        border_style="cyan"
                    ))
                    
                    # 获取答案
                    answer = Prompt.ask("\n请选择答案 (1-4)")
                    
                    if answer.lower() == 'q':
                        break
                    
                    try:
                        answer_idx = int(answer) - 1
                        if 0 <= answer_idx < len(quiz_question['options']):
                            correct = answer_idx == quiz_question['correct_index']
                            
                            if correct:
                                self.console.print("\n[bold green]✓ 回答正确！[/bold green]")
                                # 从错题集中移除（如果存在）
                                if quiz_question['command_info']['name'] in self.engine.player.wrong_commands:
                                    self.engine.player.wrong_commands.remove(quiz_question['command_info']['name'])
                            else:
                                self.console.print(f"\n[bold red]✗ 回答错误[/bold red]，正确答案是：{quiz_question['options'][quiz_question['correct_index']]}")
                                # 加入错题集
                                if quiz_question['command_info']['name'] not in self.engine.player.wrong_commands:
                                    self.engine.player.wrong_commands.append(quiz_question['command_info']['name'])
                            
                            # 显示命令详情
                            cmd_info = quiz_question['command_info']
                            self.console.print(f"\n[yellow]命令详情：[/yellow]")
                            self.console.print(f"  名称：{cmd_info['name']}")
                            self.console.print(f"  分类：{cmd_info['category']}")
                            self.console.print(f"  语法：{cmd_info['syntax']}")
                            self.console.print(f"  示例：{cmd_info['example']}")
                            self.console.print(f"  相关概念：{cmd_info['concept']}")
                            
                            self.console.print("\n" + "─" * 60)
                    except ValueError:
                        self.console.print("[red]无效输入，请输入数字[/red]")
                
                # 保存玩家进度
                self.engine.save_game()
                self.console.print("\n[green]✓ 答题进度已保存[/green]")
        except ValueError:
            self.console.print("[red]无效输入[/red]")
    
    def show_progress(self) -> None:
        """显示进度"""
        self.clear_screen()
        progress = self.engine.get_progress()
        
        player = progress["player"]
        story = progress["story"]
        commands = progress["commands"]
        
        self.console.print(Panel(
            f"[bold]当前境界：[/bold]{player['cultivation']}\n"
            f"[bold]等级：[/bold]Lv.{player['level']}\n"
            f"[bold]经验值：[/bold]{player['experience']}/{player['required_exp']}\n"
            f"[bold]总得分：[/bold]{progress['total_score']}",
            title=f"👤 {player['title']}",
            border_style="yellow"
        ))
        
        self.console.print()
        
        self.console.print(Panel(
            f"[bold]当前章节：[/bold]{story['current_title']}\n"
            f"[bold]完成进度：[/bold]{story['completed_chapters']}/{story['total_chapters']}章节\n"
            f"[bold]命令掌握：[/bold]{story['mastered_commands']}/{story['all_commands']}个",
            title="📖 故事进度",
            border_style="magenta"
        ))
        
        self.console.print()
        
        table = Table(title="📚 命令分类进度", box=box.ROUNDED)
        table.add_column("分类", style="cyan")
        table.add_column("已掌握", justify="right", style="green")
        table.add_column("总数", justify="right", style="white")
        table.add_column("进度", justify="right", style="yellow")
        
        for cat, data in commands["by_category"].items():
            table.add_row(
                cat,
                str(data["mastered"]),
                str(data["total"]),
                f"{data['percentage']}%"
            )
        
        self.console.print(Panel(table, border_style="blue"))
    
    def show_commands(self) -> None:
        """显示所有命令"""
        self.clear_screen()
        commands = self.engine.get_all_commands_info()
        
        table = Table(title="📚 Kubernetes命令手册", box=box.ROUNDED)
        table.add_column("命令", style="cyan")
        table.add_column("分类", style="magenta")
        table.add_column("描述", style="white")
        table.add_column("状态", justify="center", style="green")
        
        for cmd in commands:
            status = "✓ 已掌握" if cmd["mastered"] else "○ 待学习"
            style = "green" if cmd["mastered"] else "dim"
            table.add_row(
                cmd["name"],
                cmd["category"],
                cmd["description"],
                Text(status, style=style)
            )
        
        self.console.print(Panel(table, border_style="green"))
    
    def save_game(self, custom_name: Optional[str] = None) -> None:
        """保存游戏
        
        Args:
            custom_name: 自定义存档名称
        """
        if self.engine.save_game(custom_name):
            self.console.print("[bold green]✓ 游戏进度已保存[/bold green]")
        else:
            self.console.print("[red]保存失败[/red]")
    
    def manage_saves(self) -> None:
        """档案管理
        
        提供存档管理功能，包括查看、创建、加载、删除和重命名存档。
        """
        while True:
            self.clear_screen()
            self.console.print("[bold magenta]" + "═" * 50)
            self.console.print("[bold magenta]│  📁  档案管理  📁  │")
            self.console.print("[bold magenta]" + "═" * 50)
            self.console.print()
            
            # 显示所有存档
            saves = self.engine.get_save_list()
            
            if saves:
                self.console.print("[bold cyan]当前存档列表：[/bold cyan]")
                self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
                
                # 创建表格显示存档信息
                table = Table(show_header=True, header_style="bold green", box=box.SIMPLE)
                table.add_column("编号", justify="right", width=5)
                table.add_column("存档文件名", width=20)
                table.add_column("玩家名称", width=15)
                table.add_column("等级", justify="right", width=5)
                table.add_column("门派", width=10)
                table.add_column("境界", width=10)
                
                for idx, save in enumerate(saves, 1):
                    table.add_row(
                        str(idx),
                        save["filename"],
                        save["player_name"],
                        str(save["level"]),
                        save["sect"],
                        save["cultivation"]
                    )
                
                self.console.print(table)
                self.console.print()
            else:
                self.console.print("[yellow]暂无存档文件[/yellow]")
                self.console.print()
            
            # 显示管理选项
            self.console.print("[bold yellow]管理选项：[/bold yellow]")
            self.console.print("1. 创建新存档")
            self.console.print("2. 加载存档")
            self.console.print("3. 删除存档")
            self.console.print("4. 重命名存档")
            self.console.print("5. 返回主菜单")
            self.console.print()
            
            # 获取用户选择
            choice = Prompt.ask("请选择操作", default="5")
            
            if choice == "1":
                self.create_save()
            elif choice == "2":
                self.load_save(saves)
            elif choice == "3":
                self.delete_save(saves)
            elif choice == "4":
                self.rename_save(saves)
            elif choice == "5":
                break
            else:
                self.console.print("[red]无效选择，请重新输入[/red]")
                input("按回车键继续...")
    
    def create_save(self) -> None:
        """创建新存档
        
        提示用户输入存档名称，并保存当前游戏进度。
        """
        self.clear_screen()
        self.console.print("[bold green]📝 创建新存档[/bold green]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        # 提示用户输入存档名称
        save_name = Prompt.ask("请输入存档名称", default="")
        
        if not save_name:
            self.console.print("[red]存档名称不能为空[/red]")
            input("按回车键继续...")
            return
        
        # 保存游戏
        self.save_game(save_name)
        input("按回车键继续...")
    
    def load_save(self, saves: List[Dict[str, Any]]) -> None:
        """加载存档
        
        提示用户选择要加载的存档，并加载该存档。
        
        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return
        
        self.clear_screen()
        self.console.print("[bold blue]📂 加载存档[/bold blue]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']} - {save['player_name']} (Lv.{save['level']})")
        
        self.console.print()
        choice = Prompt.ask("请选择要加载的存档编号", default="")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                save_file = saves[idx]['filename']
                if self.engine.load_player(save_file):
                    self.console.print(f"[bold green]✓ 存档已加载：{save_file}[/bold green]")
                else:
                    self.console.print(f"[red]加载存档失败：{save_file}[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")
        
        input("按回车键继续...")
    
    def delete_save(self, saves: List[Dict[str, Any]]) -> None:
        """删除存档
        
        提示用户选择要删除的存档，并删除该存档。
        
        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return
        
        self.clear_screen()
        self.console.print("[bold red]🗑️  删除存档[/bold red]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']} - {save['player_name']} (Lv.{save['level']})")
        
        self.console.print()
        choice = Prompt.ask("请选择要删除的存档编号", default="")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                save_file = saves[idx]['filename']
                
                # 确认删除
                if Confirm.ask(f"确定要删除存档 {save_file} 吗？"):
                    if self.engine.delete_save(save_file):
                        self.console.print(f"[bold green]✓ 存档已删除：{save_file}[/bold green]")
                    else:
                        self.console.print(f"[red]删除存档失败：{save_file}[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")
        
        input("按回车键继续...")
    
    def rename_save(self, saves: List[Dict[str, Any]]) -> None:
        """重命名存档
        
        提示用户选择要重命名的存档，并输入新名称。
        
        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return
        
        self.clear_screen()
        self.console.print("[bold purple]✏️  重命名存档[/bold purple]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']}")
        
        self.console.print()
        choice = Prompt.ask("请选择要重命名的存档编号", default="")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                old_name = saves[idx]['filename']
                new_name = Prompt.ask("请输入新的存档名称", default="")
                
                if not new_name:
                    self.console.print("[red]存档名称不能为空[/red]")
                    input("按回车键继续...")
                    return
                
                # 重命名存档
                if self.engine.rename_save(old_name, new_name):
                    self.console.print(f"[bold green]✓ 存档已重命名：{old_name} → {new_name}[/bold green]")
                else:
                    self.console.print("[red]重命名存档失败[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")
        
        input("按回车键继续...")
    
    def quit_game(self) -> None:
        """退出游戏"""
        if Confirm.ask("\n确定要退出游戏吗？"):
            self.running = False
            self.console.print("\n[bold]感谢游玩KuGame！[/bold]")
            self.console.print("[italic]愿你在Kubernetes之道上一帆风顺！[/italic]\n")


def main() -> None:
    """主入口"""
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
