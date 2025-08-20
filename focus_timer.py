# focus_timer.py
import time
from datetime import timedelta

class FocusTimer:
    def __init__(self):
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60  # 5 minutes in seconds
        self.long_break_duration = 15 * 60  # 15 minutes in seconds
        self.sessions_before_long_break = 4
        
        self.reset()
    
    def reset(self):
        self.start_time = None
        self.paused_time = None
        self.is_running = False
        self.is_break = False
        self.sessions_completed = 0
        self.mode = "Ready"
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.mode = "Focus" if not self.is_break else "Break"
            
            if self.paused_time:
                # Resume from paused state
                self.start_time = time.time() - (self.paused_time - self.start_time)
                self.paused_time = None
            else:
                # Start fresh
                self.start_time = time.time()
    
    def pause(self):
        if self.is_running:
            self.is_running = False
            self.paused_time = time.time()
            self.mode = "Paused"
    
    def start_break(self):
        self.is_break = True
        self.start_time = time.time()
        self.is_running = True
        self.mode = "Break"
    
    def get_status(self):
        if not self.is_running or not self.start_time:
            return {
                "mode": self.mode,
                "time_remaining": "00:00",
                "sessions_completed": self.sessions_completed
            }
        
        elapsed = time.time() - self.start_time
        duration = self.break_duration if self.is_break else self.work_duration
        
        if elapsed >= duration:
            # Session completed
            self.is_running = False
            
            if not self.is_break:
                # Work session completed
                self.sessions_completed += 1
                self.is_break = True
                self.mode = "Break Time!"
                
                # Check if it's time for a long break
                if self.sessions_completed % self.sessions_before_long_break == 0:
                    duration = self.long_break_duration
                
                self.start_time = time.time()
                self.is_running = True
            else:
                # Break completed
                self.is_break = False
                self.mode = "Focus Time!"
                self.start_time = time.time()
                self.is_running = True
            
            # Reset elapsed time after switching mode
            elapsed = 0
        
        time_remaining = duration - elapsed
        minutes, seconds = divmod(int(time_remaining), 60)
        
        return {
            "mode": self.mode,
            "time_remaining": f"{minutes:02d}:{seconds:02d}",
            "sessions_completed": self.sessions_completed
        }