"""命令行界面

KuGame的交互式命令行界面。
"""

import sys
import os
from typing import Optional
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
    
    def __init__(self):
        self.console = Console()
        self.engine = GameEngine()
        self.running = True
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
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
    
    def print_menu(self, options):
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
    
    def start(self):
        """开始游戏"""
        self.clear_screen()
        self.print_banner()
        
        if self.engine.load_player():
            self.console.print(f"[green]✓ 欢迎回来，[/green][cyan]{self.engine.player.title}[/cyan]！")
            self.console.print()
        else:
            self.console.print("[bold yellow]新侠客，欢迎来到KuGame！[/bold yellow]\n")
            name = Prompt.ask("请输入你的侠名", default="无名")
            sect = self.get_sect_selection()
            self.engine.initialize_player(name, sect)
            self.console.print(f"\n[green]✓ 欢迎加入[/green][cyan]{sect.value}[/cyan]，{name}侠客！")
        
        self.main_loop()
    
    def main_loop(self):
        """主循环"""
        while self.running:
            self.console.print()
            options = self.engine.get_menu_options()
            self.print_menu(options)
            
            choice = Prompt.ask("\n请选择操作", default="1")
            
            self.handle_choice(choice)
    
    def handle_choice(self, choice: str):
        """处理用户选择"""
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
        elif action == "quit":
            self.quit_game()
        else:
            self.console.print("[red]无效选择，请重新输入[/red]")
    
    def play_story(self):
        """播放故事"""
        self.clear_screen()
        story = self.engine.get_story_content()
        
        self.console.print(Panel(
            story["introduction"],
            title=f"第{story['chapter_id']}章 - {story['title']}",
            border_style="magenta"
        ))
        
        self.console.print("\n[bold yellow]故事背景：[/bold yellow]")
        self.console.print(story["narrative"])
        
        self.console.print("\n[bold green]本章节将学习的命令：[/bold green]")
        for cmd in story["commands"]:
            self.console.print(f"  • {cmd}")
        
        self.console.print(f"\n[bold cyan]完成奖励：{story['reward_exp']} 经验值[/bold cyan]")
        
        if Confirm.ask("\n是否进入挑战？" if story["commands"] else "\n是否继续下一章？"):
            if story["commands"]:
                self.do_challenge()
            else:
                self.advance_story()
    
    def practice(self):
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
    
    def show_command_practice(self, command: str):
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
    
    def do_challenge(self):
        """执行挑战"""
        self.clear_screen()
        challenge = self.engine.generate_challenge()
        
        if not challenge:
            self.console.print("[yellow]暂无可用挑战[/yellow]")
            return
        
        self.console.print(Panel(
            f"[bold]挑战：{challenge.title}[/bold]\n\n"
            f"{challenge.description}\n\n"
            f"[bold]问题：[/bold]{challenge.question}\n\n"
            f"[italic]提示：{challenge.hint}[/italic]",
            title="⚔️ 挑战任务",
            border_style="red"
        ))
        
        user_answer = Prompt.ask("\n请输入你的答案")
        
        result = self.engine.check_answer(user_answer)
        
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
    
    def advance_story(self):
        """推进故事"""
        if self.engine.advance_chapter():
            self.engine.save_game()
            self.console.print("[bold green]✓ 成功进入下一章节！[/bold green]")
        else:
            self.console.print("[bold yellow]已是最终章节，恭喜你完成全部挑战！[/bold yellow]")
    
    def do_quiz(self):
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
    
    def show_progress(self):
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
    
    def show_commands(self):
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
    
    def save_game(self):
        """保存游戏"""
        if self.engine.save_game():
            self.console.print("[bold green]✓ 游戏进度已保存[/bold green]")
        else:
            self.console.print("[red]保存失败[/red]")
    
    def quit_game(self):
        """退出游戏"""
        if Confirm.ask("\n确定要退出游戏吗？"):
            self.running = False
            self.console.print("\n[bold]感谢游玩KuGame！[/bold]")
            self.console.print("[italic]愿你在Kubernetes之道上一帆风顺！[/italic]\n")


def main():
    """主入口"""
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
