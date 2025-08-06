#!/usr/bin/env python3
"""
Log monitoring script for the Agentic Framework.
Provides real-time monitoring of system logs with filtering and highlighting.
"""

import argparse
import time
import os
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class LogMonitor:
    """Real-time log monitoring utility."""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.colors = {
            'ERROR': '\033[91m',    # Red
            'WARNING': '\033[93m',  # Yellow
            'INFO': '\033[92m',     # Green
            'DEBUG': '\033[94m',    # Blue
            'RESET': '\033[0m'      # Reset
        }
    
    def colorize_log_line(self, line):
        """Add color to log lines based on level."""
        for level, color in self.colors.items():
            if f" - {level} - " in line:
                return f"{color}{line}{self.colors['RESET']}"
        return line
    
    def monitor_file(self, filename, follow=True, lines=10):
        """Monitor a specific log file."""
        filepath = self.log_dir / filename
        
        if not filepath.exists():
            print(f"Log file {filepath} does not exist.")
            return
        
        print(f"Monitoring {filepath}")
        print("=" * 60)
        
        if follow:
            # Use tail -f for real-time monitoring
            try:
                cmd = ["tail", f"-{lines}f", str(filepath)]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE, text=True)
                
                for line in iter(process.stdout.readline, ''):
                    if line:
                        colored_line = self.colorize_log_line(line.strip())
                        print(colored_line)
                        
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                process.terminate()
        else:
            # Just show last N lines
            try:
                with open(filepath, 'r') as f:
                    lines_list = f.readlines()
                    for line in lines_list[-lines:]:
                        colored_line = self.colorize_log_line(line.strip())
                        print(colored_line)
            except Exception as e:
                print(f"Error reading file: {e}")
    
    def monitor_errors_only(self, follow=True):
        """Monitor only error logs across all files."""
        print("Monitoring ERROR logs across all files")
        print("=" * 60)
        
        if follow:
            try:
                # Monitor all log files for errors
                cmd = ["tail", "-f"] + [str(f) for f in self.log_dir.glob("*.log")]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE, text=True)
                
                for line in iter(process.stdout.readline, ''):
                    if line and "ERROR" in line:
                        colored_line = self.colorize_log_line(line.strip())
                        print(f"🚨 {colored_line}")
                        
            except KeyboardInterrupt:
                print("\nError monitoring stopped.")
                process.terminate()
        else:
            # Search for recent errors
            for log_file in self.log_dir.glob("*.log"):
                try:
                    with open(log_file, 'r') as f:
                        for line_num, line in enumerate(f, 1):
                            if "ERROR" in line:
                                colored_line = self.colorize_log_line(line.strip())
                                print(f"🚨 {log_file.name}:{line_num} - {colored_line}")
                except Exception as e:
                    print(f"Error reading {log_file}: {e}")
    
    def show_summary(self):
        """Show a summary of recent log activity."""
        print("LOG SUMMARY")
        print("=" * 60)
        
        for log_file in sorted(self.log_dir.glob("*.log")):
            try:
                stat = log_file.stat()
                size_mb = stat.st_size / (1024 * 1024)
                modified = datetime.fromtimestamp(stat.st_mtime)
                
                print(f"{log_file.name:20} | {size_mb:6.2f} MB | Modified: {modified}")
                
                # Count log levels in last 50 lines
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-50:] if len(lines) > 50 else lines
                    
                    counts = {'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0}
                    for line in recent_lines:
                        for level in counts:
                            if f" - {level} - " in line:
                                counts[level] += 1
                    
                    if any(counts.values()):
                        count_str = " | ".join([f"{k}: {v}" for k, v in counts.items() if v > 0])
                        print(f"{'':20} | Recent: {count_str}")
                
                print()
                
            except Exception as e:
                print(f"Error reading {log_file}: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Monitor Agentic Framework logs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/monitor_logs.py                    # Show log summary
  python scripts/monitor_logs.py -f application    # Follow application.log
  python scripts/monitor_logs.py -e               # Monitor errors only
  python scripts/monitor_logs.py -f errors        # Follow errors.log
  python scripts/monitor_logs.py --tail 20 system # Show last 20 lines of system.log
        """
    )
    
    parser.add_argument(
        "-f", "--follow",
        metavar="LOGFILE",
        help="Follow a specific log file (without .log extension)"
    )
    
    parser.add_argument(
        "-e", "--errors-only",
        action="store_true",
        help="Monitor only ERROR level logs across all files"
    )
    
    parser.add_argument(
        "--tail",
        type=int,
        default=10,
        help="Number of lines to show when following (default: 10)"
    )
    
    parser.add_argument(
        "--no-follow",
        action="store_true",
        help="Don't follow files, just show recent lines"
    )
    
    args = parser.parse_args()
    
    monitor = LogMonitor()
    
    if args.follow:
        filename = f"{args.follow}.log"
        monitor.monitor_file(filename, follow=not args.no_follow, lines=args.tail)
    elif args.errors_only:
        monitor.monitor_errors_only(follow=not args.no_follow)
    else:
        monitor.show_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
