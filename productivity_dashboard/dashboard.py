# dashboard.py
import json
import time
import argparse
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich import box
import sys
import os

# Add the current directory to the path to ensure local imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database import TaskManager
from weather import WeatherAPI
from crypto import CryptoAPI
from focus_timer import FocusTimer
from focus_mode import FocusMode

console = Console()

class ProductivityDashboard:
    def __init__(self):
        self.config = Config()
        self.task_manager = TaskManager()
        self.weather_api = WeatherAPI(self.config)
        self.crypto_api = CryptoAPI(self.config)
        self.focus_timer = FocusTimer()
        self.focus_mode = FocusMode()
        self.layout = Layout()
        self.last_update = 0
        
    def setup_layout(self):
        # Divide the layout into sections
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Further divide the main section
        self.layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        # Divide the left section
        self.layout["left"].split(
            Layout(name="tasks"),
            Layout(name="timer")
        )
        
        # Divide the right section
        self.layout["right"].split(
            Layout(name="weather"),
            Layout(name="crypto")
        )
    
    def update_header(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_text = Text(f"Productivity Dashboard | {current_time}", style="bold blue")
        return Panel(header_text, style="white")
    
    def update_tasks(self):
        tasks = self.task_manager.get_tasks()
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("ID", style="dim", width=4)
        table.add_column("Task", min_width=20)
        table.add_column("Priority", justify="right")
        table.add_column("Status", justify="center")
        
        for task in tasks:
            priority_style = "red" if task["priority"] == "High" else "yellow" if task["priority"] == "Medium" else "green"
            status_style = "green" if task["completed"] else "red"
            status_text = "✓" if task["completed"] else "✗"
            
            table.add_row(
                str(task["id"]),
                task["description"],
                f"[{priority_style}]{task['priority']}[/{priority_style}]",
                f"[{status_style}]{status_text}[/{status_style}]"
            )
            
        return Panel(table, title="Tasks", border_style="green")
    
    def update_weather(self):
        weather_data = self.weather_api.get_weather()
        if not weather_data:
            return Panel("Weather data unavailable", title="Weather", border_style="red")
        
        weather_text = Text()
        weather_text.append(f"Location: {weather_data['city']}\n", style="bold")
        weather_text.append(f"Temperature: {weather_data['temperature']}°C\n")
        weather_text.append(f"Condition: {weather_data['description']}\n")
        weather_text.append(f"Humidity: {weather_data['humidity']}%\n")
        weather_text.append(f"Wind: {weather_data['wind_speed']} km/h")
        
        return Panel(weather_text, title="Weather", border_style="yellow")
    
    def update_crypto(self):
        crypto_data = self.crypto_api.get_crypto_prices()
        if not crypto_data:
            return Panel("Crypto data unavailable", title="Cryptocurrency", border_style="red")
        
        crypto_text = Text()
        for coin, data in crypto_data.items():
            crypto_text.append(f"{coin}: ${data['price']:,.2f}", style="bold")
            change_style = "green" if data['change_24h'] >= 0 else "red"
            crypto_text.append(f" ({data['change_24h']:+.2f}%)\n", style=change_style)
        
        return Panel(crypto_text, title="Cryptocurrency", border_style="cyan")
    
    def update_timer(self):
        timer_status = self.focus_timer.get_status()
        
        timer_text = Text()
        timer_text.append(f"Mode: {timer_status['mode']}\n", style="bold")
        timer_text.append(f"Time: {timer_status['time_remaining']}\n")
        timer_text.append(f"Session: {timer_status['sessions_completed']}/4\n")
        
        focus_status = "Active" if self.focus_mode.is_active else "Inactive"
        focus_style = "green" if self.focus_mode.is_active else "red"
        timer_text.append(f"Focus Mode: [{focus_style}]{focus_status}[/{focus_style}]")
        
        return Panel(timer_text, title="Focus Timer", border_style="magenta")
    
    def update_footer(self):
        footer_text = Text("Commands: (a)dd task, (d)elete task, (c)omplete task, (t)imer control, (f)ocus mode, (q)uit")
        return Panel(footer_text, style="white")
    
    def refresh_dashboard(self):
        self.layout["header"].update(self.update_header())
        self.layout["tasks"].update(self.update_tasks())
        self.layout["weather"].update(self.update_weather())
        self.layout["crypto"].update(self.update_crypto())
        self.layout["timer"].update(self.update_timer())
        self.layout["footer"].update(self.update_footer())
        
        return self.layout
    
    def handle_input(self, key):
        if key == "q":
            return False
        elif key == "a":
            self.add_task()
        elif key == "d":
            self.delete_task()
        elif key == "c":
            self.complete_task()
        elif key == "t":
            self.control_timer()
        elif key == "f":
            self.toggle_focus_mode()
        return True
    
    def add_task(self):
        description = console.input("Enter task description: ")
        priority = console.input("Priority (High/Medium/Low) [Medium]: ") or "Medium"
        self.task_manager.add_task(description, priority)
    
    def delete_task(self):
        task_id = console.input("Enter task ID to delete: ")
        try:
            self.task_manager.delete_task(int(task_id))
        except ValueError:
            console.print("Invalid task ID", style="red")
    
    def complete_task(self):
        task_id = console.input("Enter task ID to complete: ")
        try:
            self.task_manager.complete_task(int(task_id))
        except ValueError:
            console.print("Invalid task ID", style="red")
    
    def control_timer(self):
        console.print("Timer controls: (s)tart, (p)ause, (r)eset, (b)reak")
        action = console.input("Action: ").lower()
        
        if action == "s":
            self.focus_timer.start()
        elif action == "p":
            self.focus_timer.pause()
        elif action == "r":
            self.focus_timer.reset()
        elif action == "b":
            self.focus_timer.start_break()
    
    def toggle_focus_mode(self):
        if self.focus_mode.is_active:
            self.focus_mode.disable()
            console.print("Focus mode disabled", style="red")
        else:
            self.focus_mode.enable()
            console.print("Focus mode enabled", style="green")
    
    def run(self):
        self.setup_layout()
        
        with Live(self.refresh_dashboard(), refresh_per_second=1, screen=True) as live:
            while True:
                try:
                    # Refresh data every 30 seconds
                    current_time = time.time()
                    if current_time - self.last_update > 30:
                        live.update(self.refresh_dashboard())
                        self.last_update = current_time
                    
                    # Check for user input with a timeout
                    try:
                        # Use a non-blocking input approach
                        import select
                        import sys
                        
                        if select.select([sys.stdin], [], [], 0.1)[0]:
                            key = sys.stdin.readline().strip().lower()
                            if key and not self.handle_input(key):
                                break
                    except (ImportError, Exception):
                        # Fallback for Windows or other systems without select
                        time.sleep(0.1)
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"Error: {e}", style="red")
                    time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Intelligent CLI Productivity Dashboard")
    parser.add_argument("--setup", action="store_true", help="Run initial setup")
    args = parser.parse_args()
    
    dashboard = ProductivityDashboard()
    
    if args.setup:
        dashboard.config.setup()
    else:
        dashboard.run()

if __name__ == "__main__":
    main()