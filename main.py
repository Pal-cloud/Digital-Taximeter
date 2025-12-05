import time
import logging

# Intentar importar librerías de terminal mejorado (opcional)
try:
    from colorama import init, Fore, Back, Style
    import colorama
    colorama.init()  # Para Windows
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

# Configuración simple de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/taximeter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def print_colored(message, color=None, style=None):
    """Imprimir con colores si está disponible, sino texto normal."""
    if COLORS_AVAILABLE and color:
        color_code = getattr(Fore, color.upper(), '')
        style_code = getattr(Style, style.upper(), '') if style else ''
        reset = Style.RESET_ALL
        print(f"{style_code}{color_code}{message}{reset}")
    else:
        print(message)

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros
    stopped: 0.02€/s
    moving: 0.05€/s
    """
    logging.info(f"Calculando tarifa: parado={seconds_stopped:.1f}s, movimiento={seconds_moving:.1f}s")
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    # Redondear a 2 decimales para evitar problemas de precisión con dinero
    fare = round(fare, 2)
    print_colored(f"Este es el total: €{fare}", "green", "bright")
    return fare

def taximeter():
    """
    Funcion principal del taximetro: manejar y mostrar opciones.
    """
    print_colored("🚕 Welcome to Digital Taxi 🚕", "cyan", "bright")
    print_colored("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n", "yellow")
    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

    while True:
        command = input("🚕 > ").strip().lower()

        if command == 'start':
            if trip_active:
                logging.warning("Intento de iniciar viaje con trip activo")
                print_colored("❌ Error: Trip already in progress.", "red")
                continue
            trip_active = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            logging.info("Viaje iniciado")
            print_colored("✅ Trip started. Initial state: 'stopped'", "green")

        elif command in ("stop", "move"):
            if not trip_active:
                logging.warning("Comando de estado sin viaje activo")
                print_colored("❌ Error: No active trip. Use 'start' to begin.", "red")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration

            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()
            logging.info(f"Estado cambiado a: {state}")
            
            if state == "stopped":
                print_colored(f"🛑 State changed to '{state}'.", "yellow")
            else:
                print_colored(f"🚗 State changed to '{state}'.", "cyan")

        elif command == 'finish':
            if not trip_active:
                logging.warning("Intento de finalizar viaje sin trip activo")
                print_colored("❌ Error: No active trip to finish.", "red")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration

            total_fare = calculate_fare(stopped_time, moving_time)
            logging.info(f"Viaje finalizado - Tiempo parado: {stopped_time:.1f}s, Tiempo movimiento: {moving_time:.1f}s")
            logging.info(f"Tarifa total calculada: €{total_fare:.2f}")
            
            print_colored("\n📊 --- Trip Summary ---", "magenta", "bright")
            print(f"⏱️  Stopped time: {stopped_time:.1f} seconds")
            print(f"🚗 Moving time: {moving_time:.1f} seconds")
            print_colored(f"💰 Total fare: €{total_fare:.2f}", "green", "bright")
            print_colored("📊 ---------------------\n", "magenta", "bright")

            trip_active = False
            state = None

        elif command == 'exit':
            logging.info("Usuario salió de la aplicación")
            print_colored("👋 Exiting Digital Taxi. Goodbye!", "cyan", "bright")
            break
        else:
            logging.warning(f"Comando inválido recibido: '{command}'")
            print_colored("❓ Invalid command. Please use 'start', 'stop', 'move', 'finish', or 'exit'.", "red")

if __name__ == "__main__":
    logging.info("Iniciando Digital Taximeter")
    taximeter()