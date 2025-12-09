"""
Digital Taximeter - Core functionality
Professional taxi fare calculation system with enhanced visual interface
"""
import time
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.settings import FARE_RATES, setup_logging
    from src.utils import print_colored, clear_screen, format_currency, format_time
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.settings import FARE_RATES, setup_logging
    from src.utils import print_colored, clear_screen, format_currency, format_time

# ASCII Art for taxi animation and interface
TAXI_FRAMES = [
    "    🚕💨     ",
    "   🚕💨      ",
    "  🚕💨       ",
    " 🚕💨        ",
    "🚕💨         ",
    " 🚕💨        ",
    "  🚕💨       ",
    "   🚕💨      "
]

TAXI_LOGO = """
╔════════════════════════════════════════════╗
║           🚕 DIGITAL TAXIMETER 🚕           ║
║                                            ║
║    Professional Fare Calculation System    ║
╚════════════════════════════════════════════╝
"""

HELP_MENU = """
📋 Available Commands:
┌─────────────────────────────────────────┐
│ 🚀 start   │ Begin a new trip           │
│ 🛑 stop    │ Set taxi to stopped state  │
│ 🚗 move    │ Set taxi to moving state   │
│ 🏁 finish  │ Complete trip & calculate  │
│ 📊 status  │ Show current trip status   │
│ 📋 help    │ Show this menu             │
│ 🚪 exit    │ Exit the application       │
└─────────────────────────────────────────┘
"""

class TaxiMeter:
    """Professional taxi meter with state management and fare calculation."""
    
    def __init__(self):
        self.trip_active = False
        self.start_time = 0
        self.stopped_time = 0
        self.moving_time = 0
        self.state = None
        self.state_start_time = 0
        
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def calculate_fare(self):
        """Calculate total fare based on stopped and moving time."""
        fare = (self.stopped_time * FARE_RATES['stopped'] + 
                self.moving_time * FARE_RATES['moving'])
        return round(fare, 2)
    
    def start_trip(self):
        """Start a new taxi trip with enhanced visual feedback."""
        if self.trip_active:
            self.logger.warning("Attempt to start trip while trip already active")
            print_colored("❌ Error: Trip already in progress.", "red")
            return False
            
        self.trip_active = True
        self.start_time = time.time()
        self.stopped_time = 0
        self.moving_time = 0
        self.state = 'stopped'
        self.state_start_time = time.time()
        
        self.logger.info("Trip started")
        print_colored("✅ Trip started successfully!", "green", "bright")
        print_colored("🛑 Initial state: STOPPED", "yellow")
        return True
    
    def change_state(self, new_state):
        """Change taxi state between 'stopped' and 'moving' with enhanced feedback."""
        if not self.trip_active:
            self.logger.warning("State change command without active trip")
            print_colored("❌ Error: No active trip.", "red")
            print_colored("💡 Use 'start' to begin a new trip.", "yellow")
            return False
            
        # Calculate time in previous state
        duration = time.time() - self.state_start_time
        if self.state == 'stopped':
            self.stopped_time += duration
        else:
            self.moving_time += duration
            
        self.state = new_state
        self.state_start_time = time.time()
        
        self.logger.info(f"State changed to: {new_state}")
        
        if new_state == "stopped":
            print_colored("🛑 State changed to: STOPPED", "yellow", "bright")
        else:
            print_colored("🚗 State changed to: MOVING", "cyan", "bright")
            
        return True
    
    def finish_trip(self):
        """Finish the current trip and calculate final fare."""
        if not self.trip_active:
            self.logger.warning("Attempt to finish trip without active trip")
            print_colored("❌ Error: No active trip to finish.", "red")
            print_colored("💡 Use 'start' to begin a new trip.", "yellow")
            return None
            
        # Calculate final time in current state
        duration = time.time() - self.state_start_time
        if self.state == 'stopped':
            self.stopped_time += duration
        else:
            self.moving_time += duration
            
        total_fare = self.calculate_fare()
        
        self.logger.info(f"Trip finished - Stopped: {self.stopped_time:.1f}s, Moving: {self.moving_time:.1f}s")
        self.logger.info(f"Total fare calculated: {format_currency(total_fare)}")
        
        # Display enhanced trip summary
        print_colored("\n" + "="*50, "magenta", "bright")
        print_colored("🏁 TRIP COMPLETED - FARE SUMMARY", "magenta", "bright")
        print_colored("="*50, "magenta", "bright")
        print(f"⏱️  Time stopped:  {format_time(self.stopped_time)}  ({format_currency(self.stopped_time * FARE_RATES['stopped'])})")
        print(f"🚗 Time moving:   {format_time(self.moving_time)}  ({format_currency(self.moving_time * FARE_RATES['moving'])})")
        print_colored("─" * 50, "white")
        print_colored(f"💰 TOTAL FARE:    {format_currency(total_fare)}", "green", "bright")
        print_colored("="*50 + "\n", "magenta", "bright")
        
        # Reset trip state
        self.trip_active = False
        self.state = None
        
        return total_fare

def animate_taxi():
    """Show a simple taxi startup message."""
    try:
        from config.settings import COLORS_AVAILABLE
    except ImportError:
        COLORS_AVAILABLE = False
    
    print_colored("🚀 Starting Digital Taximeter... 🚕💨", "cyan", "bright")
    time.sleep(0.3)  # Brief pause
    print()

def show_welcome():
    """Display the welcome screen with logo and menu."""
    clear_screen()
    
    # Try to display with colors, fallback to plain text if needed
    try:
        print_colored(TAXI_LOGO, "cyan", "bright")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Fallback ASCII logo for terminals with encoding issues
        fallback_logo = """
+============================================+
|           🚕 DIGITAL TAXIMETER 🚕           |
|                                            |
|    Professional Fare Calculation System    |
+============================================+
"""
        print_colored(fallback_logo, "cyan", "bright")
    
    animate_taxi()
    print_colored(HELP_MENU, "yellow")
    print_colored("💡 Tip: Type 'help' anytime to see this menu again!", "green")
    print()

def show_status(trip_active, state, stopped_time, moving_time):
    """Display current trip status."""
    if trip_active:
        status_color = "green" if state == "moving" else "yellow"
        status_emoji = "🚗" if state == "moving" else "🛑"
        print_colored(f"\n📊 Current Status: {status_emoji} {state.upper()}", status_color, "bright")
        print(f"⏱️  Time stopped: {stopped_time:.1f}s | Time moving: {moving_time:.1f}s")
        estimated_fare = stopped_time * FARE_RATES['stopped'] + moving_time * FARE_RATES['moving']
        print_colored(f"💰 Estimated fare: {format_currency(estimated_fare)}", "magenta")
        print()
    else:
        print_colored("\n📍 Status: No active trip", "red")
        print_colored("💡 Use 'start' to begin a new trip", "yellow")
        print()

def main():
    """Main application entry point with enhanced visual interface."""
    meter = TaxiMeter()
    meter.logger.info("Starting Digital Taximeter")
    
    # Show enhanced welcome screen
    show_welcome()
    
    while True:
        try:
            # Dynamic prompt based on taxi state
            if meter.trip_active:
                if meter.state == "moving":
                    prompt = "� moving > "
                else:
                    prompt = "🛑 stopped > "
                print_colored(prompt, "cyan", end="")
            else:
                print_colored("🚕 taxi > ", "yellow", end="")
            
            command = input().strip().lower()
            
            if command == 'help':
                print_colored(HELP_MENU, "yellow")
                continue
                
            elif command == 'status':
                show_status(meter.trip_active, meter.state, meter.stopped_time, meter.moving_time)
                continue
                
            elif command == 'start':
                if meter.start_trip():
                    print_colored("💡 Use 'move' when the taxi starts moving", "cyan")
                else:
                    print_colored("💡 Use 'finish' to complete current trip first.", "yellow")
                
            elif command == 'stop':
                if meter.change_state('stopped'):
                    show_status(meter.trip_active, meter.state, meter.stopped_time, meter.moving_time)
                
            elif command == 'move':
                if meter.change_state('moving'):
                    show_status(meter.trip_active, meter.state, meter.stopped_time, meter.moving_time)
                
            elif command == 'finish':
                meter.finish_trip()
                
            elif command == 'exit':
                if meter.trip_active:
                    print_colored("⚠️  Warning: You have an active trip!", "yellow")
                    confirm = input("🤔 Do you want to finish the trip first? (y/n): ").strip().lower()
                    if confirm == 'y':
                        # Auto-finish the trip
                        total_fare = meter.finish_trip()
                        if total_fare:
                            print_colored(f"🏁 Auto-completed trip. Final fare: {format_currency(total_fare)}", "green")
                            meter.logger.info(f"Trip auto-completed on exit - Fare: {format_currency(total_fare)}")
                
                meter.logger.info("User exited application")
                print_colored("\n🌟 Thank you for using Digital Taximeter!", "cyan", "bright")
                print_colored("👋 Goodbye and safe travels!", "yellow")
                break
                
            else:
                meter.logger.warning(f"Invalid command received: '{command}'")
                print_colored(f"❓ Unknown command: '{command}'", "red")
                print_colored("💡 Type 'help' to see available commands.", "yellow")
                
        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye!", "cyan", "bright")
            break
        except Exception as e:
            meter.logger.error(f"Unexpected error: {e}")
            print_colored(f"❌ An error occurred: {e}", "red")

if __name__ == "__main__":
    show_welcome()
    main()
