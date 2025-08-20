# focus_mode.py
import platform
import os
import tempfile
from pathlib import Path

class FocusMode:
    def __init__(self):
        self.hosts_path = self.get_hosts_path()
        self.blocked_sites = []
        self.is_active = False
    
    def get_hosts_path(self):
        if platform.system() == "Windows":
            return Path("C:/Windows/System32/drivers/etc/hosts")
        else:
            return Path("/etc/hosts")
    
    def enable(self, sites=None):
        if sites:
            self.blocked_sites = sites
        
        if not self.blocked_sites:
            return False
        
        try:
            # Backup current hosts file
            with open(self.hosts_path, 'r') as f:
                original_content = f.read()
            
            # Add blocked sites to hosts file
            with open(self.hosts_path, 'a') as f:
                f.write("\n# Productivity Dashboard Focus Mode\n")
                for site in self.blocked_sites:
                    f.write(f"127.0.0.1 {site}\n")
                    f.write(f"127.0.0.1 www.{site}\n")
            
            self.is_active = True
            return True
            
        except PermissionError:
            print("Permission denied. Try running as administrator/root.")
            return False
        except Exception as e:
            print(f"Error enabling focus mode: {e}")
            return False
    
    def disable(self):
        try:
            # Read current hosts file
            with open(self.hosts_path, 'r') as f:
                lines = f.readlines()
            
            # Remove our entries
            new_lines = []
            in_block = False
            
            for line in lines:
                if line.strip() == "# Productivity Dashboard Focus Mode":
                    in_block = True
                    continue
                if in_block and line.startswith("127.0.0.1"):
                    continue
                if in_block and not line.startswith("127.0.0.1"):
                    in_block = False
                
                if not in_block:
                    new_lines.append(line)
            
            # Write cleaned hosts file
            with open(self.hosts_path, 'w') as f:
                f.writelines(new_lines)
            
            self.is_active = False
            return True
            
        except PermissionError:
            print("Permission denied. Try running as administrator/root.")
            return False
        except Exception as e:
            print(f"Error disabling focus mode: {e}")
            return False
    
    def is_active(self):
        return self.is_active