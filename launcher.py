"""
TickZero Launcher - Unified entry point for CS2 Highlights Generator.
Provides user-friendly menu interface for all application features.
"""
import os
import sys
import json
import time
import subprocess
import webbrowser
import threading
from pathlib import Path

# ANSI color codes for better UI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class TickZeroLauncher:
    """Main launcher application."""
    
    def __init__(self):
        self.config_file = Path("config.json")
        self.config = self.load_config()
        self.web_server_process = None
    
    def load_config(self):
        """Load configuration from JSON file."""
        default_config = {
            "obs_host": "localhost",
            "obs_port": 4455,
            "obs_password": "",
            "gsi_port": 3000,
            "use_gpu": True,
            "auto_recording": True,
            "continuous_mode": True,
            "auto_process": True,
            "auto_min_priority": 6,
            "web_port": 5000,
            "db_path": "matches.db",
            "log_file": "match_log.json",
            "output_dir": "highlights"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"{Colors.YELLOW}Warning: Could not load config file. Using defaults.{Colors.END}")
        else:
            # Create default config file
            self.save_config(default_config)
        
        return default_config
    
    def save_config(self, config=None):
        """Save configuration to JSON file."""
        if config is None:
            config = self.config
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def clear_screen(self):
        """Clear the console screen."""
        # Use subprocess instead of os.system for security
        try:
            if os.name == 'nt':
                subprocess.run(['cmd', '/c', 'cls'], check=False)
            else:
                subprocess.run(['clear'], check=False)
        except:
            # Fallback: print newlines
            print('\n' * 50)
    
    def show_header(self):
        """Display application header."""
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  TickZero - CS2 Highlights Generator".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "=" * 58 + "╝")
        print(f"{Colors.END}")
    
    def show_menu(self):
        """Display main menu and get user choice."""
        self.clear_screen()
        self.show_header()
        
        print(f"\n{Colors.BOLD}Main Menu:{Colors.END}\n")
        print(f"  {Colors.GREEN}[1]{Colors.END} 🎮 Start Recording Session")
        print(f"  {Colors.GREEN}[2]{Colors.END} 🌐 Open Match History Browser")
        print(f"  {Colors.GREEN}[3]{Colors.END} ✂️  Process Video File")
        print(f"  {Colors.GREEN}[4]{Colors.END} ⚙️  Settings")
        print(f"  {Colors.GREEN}[5]{Colors.END} ℹ️  Help & Documentation")
        print(f"  {Colors.GREEN}[6]{Colors.END} 🚪 Exit")
        
        print("\n" + "─" * 60)
        choice = input(f"\n{Colors.BOLD}Select option (1-6):{Colors.END} ").strip()
        return choice
    
    def start_recording(self):
        """Start live recording session."""
        self.clear_screen()
        self.show_header()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Starting Recording Session...{Colors.END}\n")
        
        print("This will:")
        print("  • Connect to OBS WebSocket")
        print("  • Start GSI server on port 3000")
        print("  • Wait for CS2 match to begin")
        print("  • Automatically record gameplay")
        print("  • Save match to history database")
        
        if self.config.get('continuous_mode'):
            print(f"\n{Colors.CYAN}Continuous mode enabled - will record multiple matches{Colors.END}")
        
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop recording{Colors.END}\n")
        time.sleep(2)
        
        try:
            subprocess.run([sys.executable, "main.py", "live"])
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Recording stopped by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.END}")
        
        input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
    
    def open_browser_ui(self):
        """Launch web interface and open browser."""
        self.clear_screen()
        self.show_header()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Starting Match History Browser...{Colors.END}\n")
        
        port = self.config.get('web_port', 5000)
        url = f"http://localhost:{port}"
        
        # Start web server in background thread
        def run_server():
            try:
                from web_interface import run_web_interface
                run_web_interface(port=port, debug=False)
            except Exception as e:
                print(f"{Colors.RED}Error starting web server: {e}{Colors.END}")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("Starting web server...")
        time.sleep(3)
        
        # Open browser
        print(f"Opening browser at {url}...")
        try:
            webbrowser.open(url)
            print(f"\n{Colors.GREEN}✓ Web interface is running!{Colors.END}")
            print(f"{Colors.CYAN}URL: {url}{Colors.END}\n")
            print(f"{Colors.YELLOW}Press Ctrl+C to close the web interface{Colors.END}\n")
            
            # Keep running until Ctrl+C
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Closing web interface...{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}Error opening browser: {e}{Colors.END}")
            print(f"Please open manually: {url}")
        
        input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
    
    def process_video(self):
        """Process a video file to generate highlights."""
        self.clear_screen()
        self.show_header()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Process Video File{Colors.END}\n")
        
        print("Enter the path to your recorded CS2 match video:")
        video_path = input(f"{Colors.CYAN}Video path:{Colors.END} ").strip().strip('"')
        
        # Validate file path exists and is a file (security: prevent path traversal)
        try:
            video_file = Path(video_path).resolve()
            if not video_file.exists() or not video_file.is_file():
                print(f"{Colors.RED}Error: File not found or invalid{Colors.END}")
                input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
                return
            # Convert to absolute path string for safety
            video_path = str(video_file)
        except (OSError, ValueError) as e:
            print(f"{Colors.RED}Error: Invalid file path{Colors.END}")
            input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
            return
        
        print(f"\nMinimum priority for highlights (1-10, default: {self.config.get('auto_min_priority', 6)}):")
        priority_input = input(f"{Colors.CYAN}Priority:{Colors.END} ").strip()
        
        try:
            min_priority = int(priority_input) if priority_input else self.config.get('auto_min_priority', 6)
        except:
            min_priority = 6
        
        print(f"\n{Colors.YELLOW}Processing highlights...{Colors.END}\n")
        
        try:
            subprocess.run([sys.executable, "main.py", "process", video_path, str(min_priority)])
            print(f"\n{Colors.GREEN}✓ Processing complete!{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.END}")
        
        input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
    
    def settings(self):
        """Configuration settings menu."""
        while True:
            self.clear_screen()
            self.show_header()
            print(f"\n{Colors.BOLD}Settings:{Colors.END}\n")
            
            print(f"  {Colors.GREEN}[1]{Colors.END} OBS WebSocket Settings")
            print(f"      Host: {self.config.get('obs_host')} | Port: {self.config.get('obs_port')}")
            print(f"\n  {Colors.GREEN}[2]{Colors.END} Recording Settings")
            print(f"      Auto-recording: {self.config.get('auto_recording')}")
            print(f"      Continuous mode: {self.config.get('continuous_mode')}")
            print(f"\n  {Colors.GREEN}[3]{Colors.END} Highlight Processing")
            print(f"      Auto-process: {self.config.get('auto_process')}")
            print(f"      Min priority: {self.config.get('auto_min_priority')}")
            print(f"      GPU: {self.config.get('use_gpu')}")
            print(f"\n  {Colors.GREEN}[4]{Colors.END} Test OBS Connection")
            print(f"  {Colors.GREEN}[5]{Colors.END} View Configuration File")
            print(f"  {Colors.GREEN}[0]{Colors.END} Back to Main Menu")
            
            choice = input(f"\n{Colors.BOLD}Select option:{Colors.END} ").strip()
            
            if choice == '1':
                self._edit_obs_settings()
            elif choice == '2':
                self._edit_recording_settings()
            elif choice == '3':
                self._edit_processing_settings()
            elif choice == '4':
                self._test_obs_connection()
            elif choice == '5':
                self._view_config()
            elif choice == '0':
                break
    
    def _edit_obs_settings(self):
        """Edit OBS WebSocket settings."""
        print(f"\n{Colors.BOLD}OBS WebSocket Settings:{Colors.END}")
        
        host = input(f"Host [{self.config['obs_host']}]: ").strip() or self.config['obs_host']
        port_input = input(f"Port [{self.config['obs_port']}]: ").strip()
        port = int(port_input) if port_input else self.config['obs_port']
        password = input(f"Password (leave empty if none): ").strip()
        
        self.config['obs_host'] = host
        self.config['obs_port'] = port
        if password:
            self.config['obs_password'] = password
        
        self.save_config()
        print(f"{Colors.GREEN}✓ Settings saved{Colors.END}")
        time.sleep(1)
    
    def _edit_recording_settings(self):
        """Edit recording settings."""
        print(f"\n{Colors.BOLD}Recording Settings:{Colors.END}")
        
        auto_rec = input(f"Auto-recording [y/n, current: {'y' if self.config['auto_recording'] else 'n'}]: ").strip().lower()
        if auto_rec in ['y', 'n']:
            self.config['auto_recording'] = auto_rec == 'y'
        
        cont_mode = input(f"Continuous mode [y/n, current: {'y' if self.config['continuous_mode'] else 'n'}]: ").strip().lower()
        if cont_mode in ['y', 'n']:
            self.config['continuous_mode'] = cont_mode == 'y'
        
        self.save_config()
        print(f"{Colors.GREEN}✓ Settings saved{Colors.END}")
        time.sleep(1)
    
    def _edit_processing_settings(self):
        """Edit processing settings."""
        print(f"\n{Colors.BOLD}Highlight Processing Settings:{Colors.END}")
        
        auto_proc = input(f"Auto-process [y/n, current: {'y' if self.config['auto_process'] else 'n'}]: ").strip().lower()
        if auto_proc in ['y', 'n']:
            self.config['auto_process'] = auto_proc == 'y'
        
        priority_input = input(f"Min priority [1-10, current: {self.config['auto_min_priority']}]: ").strip()
        if priority_input:
            try:
                self.config['auto_min_priority'] = int(priority_input)
            except:
                pass
        
        gpu = input(f"Use GPU [y/n, current: {'y' if self.config['use_gpu'] else 'n'}]: ").strip().lower()
        if gpu in ['y', 'n']:
            self.config['use_gpu'] = gpu == 'y'
        
        self.save_config()
        print(f"{Colors.GREEN}✓ Settings saved{Colors.END}")
        time.sleep(1)
    
    def _test_obs_connection(self):
        """Test OBS WebSocket connection."""
        print(f"\n{Colors.BOLD}Testing OBS Connection...{Colors.END}\n")
        
        try:
            from obs_manager import OBSManager
            obs = OBSManager(
                host=self.config['obs_host'],
                port=self.config['obs_port'],
                password=self.config.get('obs_password', '')
            )
            
            if obs.connect():
                print(f"{Colors.GREEN}✓ Successfully connected to OBS!{Colors.END}")
                obs.disconnect()
            else:
                print(f"{Colors.RED}✗ Failed to connect to OBS{Colors.END}")
                print("\nMake sure:")
                print("  • OBS Studio is running")
                print("  • WebSocket server is enabled in OBS")
                print("  • Port and password match your OBS settings")
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def _view_config(self):
        """View configuration file."""
        print(f"\n{Colors.BOLD}Current Configuration:{Colors.END}\n")
        print(json.dumps(self.config, indent=2))
        print(f"\nConfig file location: {self.config_file.absolute()}")
        input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.END}")
    
    def show_help(self):
        """Display help and documentation."""
        self.clear_screen()
        self.show_header()
        print(f"\n{Colors.BOLD}Help & Documentation{Colors.END}\n")
        
        print(f"{Colors.CYAN}Quick Start:{Colors.END}")
        print("  1. Configure OBS WebSocket (Settings menu)")
        print("  2. Set up CS2 Game State Integration (copy cfg file)")
        print("  3. Get Google Gemini API key")
        print("  4. Start recording session and play CS2")
        print("  5. Browse match history and generate highlights")
        
        print(f"\n{Colors.CYAN}Requirements:{Colors.END}")
        print("  • OBS Studio with WebSocket enabled")
        print("  • Counter-Strike 2")
        print("  • Google Gemini API key (free)")
        print("  • FFmpeg installed")
        
        print(f"\n{Colors.CYAN}Documentation:{Colors.END}")
        print("  • README.md - Full documentation")
        print("  • MATCH_HISTORY.md - Match history system guide")
        
        print(f"\n{Colors.CYAN}Support:{Colors.END}")
        print("  • GitHub: https://github.com/MACULINX/TickZero")
        
        input(f"\n{Colors.BOLD}Press Enter to return to main menu...{Colors.END}")
    
    def run(self):
        """Main application loop."""
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.start_recording()
            elif choice == '2':
                self.open_browser_ui()
            elif choice == '3':
                self.process_video()
            elif choice == '4':
                self.settings()
            elif choice == '5':
                self.show_help()
            elif choice == '6':
                self.clear_screen()
                print(f"\n{Colors.CYAN}Thanks for using TickZero!{Colors.END}\n")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Invalid option. Please try again.{Colors.END}")
                time.sleep(1)


def main():
    """Main entry point."""
    # Handle command-line arguments for direct access
    if len(sys.argv) > 1:
        launcher = TickZeroLauncher()
        
        if sys.argv[1] == '--record':
            launcher.start_recording()
        elif sys.argv[1] == '--browse':
            launcher.open_browser_ui()
        elif sys.argv[1] == '--process' and len(sys.argv) > 2:
            launcher.process_video()
        elif sys.argv[1] == '--help':
            launcher.show_help()
        else:
            print("Unknown command. Use: --record, --browse, --process, --help")
    else:
        # Interactive menu
        launcher = TickZeroLauncher()
        launcher.run()


if __name__ == '__main__':
    main()
