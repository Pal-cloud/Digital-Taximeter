import time
import logging

# Configuración simple de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('taximeter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros
    stopped: 0.02€/s
    moving: 0.05€/s
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    print(f"Este es el total: {fare}€")
    return fare

def taximeter():
    """
    Funcion principal del taximetro: manejar y mostrar opciones.
    """
    print("Welcome to Digital Taxi")
    print("Available commands:'start', 'stop', 'move', 'finish', 'exit'\n")
    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

    while True:
        command = input("> ").strip().lower()

        if command == 'start':
            if trip_active:
                print("Error: Trip already in progress.")
                continue
            trip_active = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            print("Trip started. Initial state: 'stopped'")

        elif command in ("stop", "move"):
            if not trip_active:
                print("Error: No active trip. Use 'start' to begin.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration

            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()
            print(f"State changed to '{state}'.")

        elif command == 'finish':
            if not trip_active:
                print("Error: No active trip to finish.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration

            total_fare = calculate_fare(stopped_time, moving_time)
            print("\n--- Trip Summary ---")
            print(f"Stopped time: {stopped_time:.1f} seconds")
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}")
            print("---------------------\n")

            trip_active = False
            state = None

        elif command == 'exit':
            print("Exiting Digital Taxi. Goodbye!")
            break
        else:
            print("Invalid command. Please use 'start', 'stop', 'move', 'finish', or 'exit'.")

if __name__ == "__main__":
    logging.info("Iniciando Digital Taximeter")
    taximeter()