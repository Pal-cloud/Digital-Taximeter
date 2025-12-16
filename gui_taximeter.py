# -*- coding: utf-8 -*-
"""
Digital Taximeter - GUI Version
Sistema de Taxímetro Digital con Interfaz Gráfica
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import time
import threading
from datetime import datetime
import os
import logging

# Importar las funciones del taxímetro original
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar las funciones del taxímetro original
import main as taximeter_main
from main import calculate_fare, save_trip_to_history, PRICE_PROFILES, change_price_profile

class TaximeterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        self.reset_trip()
        
        # Timer para actualizar el display
        self.update_timer()
    
    def setup_window(self):
        """Configurar la ventana principal"""
        self.root.title("🚖 Digital Taximeter - Interfaz Gráfica")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Centrar la ventana
        self.center_window()
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Hacer la ventana redimensionable pero con límites
        self.root.minsize(700, 500)
        self.root.maxsize(1200, 800)
        
        # Icono y configuración
        try:
            self.root.iconify()  # Minimizar y restaurar para forzar icono
            self.root.deiconify()
        except:
            pass
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{800}x{600}+{x}+{y}')
    
    def setup_variables(self):
        """Configurar las variables del taxímetro"""
        self.trip_active = False
        self.state = "stopped"  # stopped, moving
        self.start_time = 0
        self.stopped_time = 0
        self.moving_time = 0
        self.current_state_start = 0
        self.timer_running = False
        
        # Variables de la interfaz
        self.status_var = tk.StringVar(value="🚖 Listo para iniciar viaje")
        self.time_stopped_var = tk.StringVar(value="0.0")
        self.time_moving_var = tk.StringVar(value="0.0")
        self.fare_var = tk.StringVar(value="€0.00")
        self.profile_var = tk.StringVar(value="Normal")
    
    def setup_styles(self):
        """Configurar estilos personalizados"""
        self.colors = {
            'bg_dark': '#1e1e1e',
            'bg_light': '#2d2d2d', 
            'accent': '#0078d4',
            'success': '#107c10',
            'warning': '#ffb900',
            'error': '#d13438',
            'text': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
        # Fuentes personalizadas
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'subtitle': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'large_num': ('Consolas', 24, 'bold'),
            'med_num': ('Consolas', 14, 'bold')
        }
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        self.create_header(main_frame)
        
        # Frame de estado y controles
        self.create_status_section(main_frame)
        
        # Frame de tiempos y tarifa
        self.create_metrics_section(main_frame)
        
        # Frame de controles principales
        self.create_controls_section(main_frame)
        
        # Frame de perfiles de tarifa
        self.create_pricing_section(main_frame)
        
        # Frame de historial
        self.create_history_section(main_frame)
    
    def create_header(self, parent):
        """Crear la cabecera del programa"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="🚖 DIGITAL TAXIMETER",
            font=self.fonts['title'],
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(
            header_frame,
            text="Sistema Profesional de Cálculo de Tarifas",
            font=self.fonts['body'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_dark']
        )
        subtitle_label.pack()
    
    def create_status_section(self, parent):
        """Crear la sección de estado"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief='raised', bd=2)
        status_frame.pack(fill='x', pady=(0, 15))
        
        # Label de estado
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=self.fonts['subtitle'],
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        )
        self.status_label.pack(pady=10)
    
    def create_metrics_section(self, parent):
        """Crear la sección de métricas (tiempos y tarifa)"""
        metrics_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        metrics_frame.pack(fill='x', pady=(0, 15))
        
        # Frame para tiempo parado
        stopped_frame = tk.Frame(metrics_frame, bg=self.colors['bg_light'], relief='raised', bd=2)
        stopped_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tk.Label(
            stopped_frame,
            text="🛑 TIEMPO PARADO",
            font=self.fonts['body'],
            fg=self.colors['warning'],
            bg=self.colors['bg_light']
        ).pack(pady=(10, 5))
        
        tk.Label(
            stopped_frame,
            textvariable=self.time_stopped_var,
            font=self.fonts['med_num'],
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        ).pack(pady=(0, 5))
        
        tk.Label(
            stopped_frame,
            text="segundos",
            font=self.fonts['body'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(pady=(0, 10))
        
        # Frame para tiempo en movimiento
        moving_frame = tk.Frame(metrics_frame, bg=self.colors['bg_light'], relief='raised', bd=2)
        moving_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(
            moving_frame,
            text="🏃 TIEMPO MOVIMIENTO",
            font=self.fonts['body'],
            fg=self.colors['success'],
            bg=self.colors['bg_light']
        ).pack(pady=(10, 5))
        
        tk.Label(
            moving_frame,
            textvariable=self.time_moving_var,
            font=self.fonts['med_num'],
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        ).pack(pady=(0, 5))
        
        tk.Label(
            moving_frame,
            text="segundos",
            font=self.fonts['body'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        ).pack(pady=(0, 10))
        
        # Frame para tarifa
        fare_frame = tk.Frame(metrics_frame, bg=self.colors['accent'], relief='raised', bd=2)
        fare_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(
            fare_frame,
            text="💰 TARIFA ACTUAL",
            font=self.fonts['body'],
            fg='white',
            bg=self.colors['accent']
        ).pack(pady=(10, 5))
        
        tk.Label(
            fare_frame,
            textvariable=self.fare_var,
            font=self.fonts['large_num'],
            fg='white',
            bg=self.colors['accent']
        ).pack(pady=(0, 10))
    
    def create_controls_section(self, parent):
        """Crear la sección de controles principales"""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        controls_frame.pack(fill='x', pady=(0, 15))
        
        # Botón iniciar/finalizar
        self.start_finish_btn = tk.Button(
            controls_frame,
            text="🚀 INICIAR VIAJE",
            font=self.fonts['subtitle'],
            command=self.toggle_trip,
            bg=self.colors['success'],
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=10
        )
        self.start_finish_btn.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Botón parar/mover
        self.stop_move_btn = tk.Button(
            controls_frame,
            text="🛑 PARAR",
            font=self.fonts['subtitle'],
            command=self.toggle_state,
            bg=self.colors['warning'],
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=10,
            state='disabled'
        )
        self.stop_move_btn.pack(side='left', fill='both', expand=True, padx=5)
        
        # Botón historial
        history_btn = tk.Button(
            controls_frame,
            text="📜 HISTORIAL",
            font=self.fonts['subtitle'],
            command=self.show_history,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            relief='raised',
            bd=3,
            padx=20,
            pady=10
        )
        history_btn.pack(side='left', fill='both', expand=True, padx=(5, 0))
    
    def create_pricing_section(self, parent):
        """Crear la sección de perfiles de tarifa"""
        pricing_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief='raised', bd=2)
        pricing_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            pricing_frame,
            text="💰 PERFILES DE TARIFA",
            font=self.fonts['subtitle'],
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        ).pack(pady=(10, 5))
        
        # Combobox para seleccionar perfil
        profile_frame = tk.Frame(pricing_frame, bg=self.colors['bg_light'])
        profile_frame.pack(pady=(0, 10))
        
        tk.Label(
            profile_frame,
            text="Perfil activo:",
            font=self.fonts['body'],
            fg=self.colors['text'],
            bg=self.colors['bg_light']
        ).pack(side='left', padx=(10, 5))
        
        self.profile_combo = ttk.Combobox(
            profile_frame,
            textvariable=self.profile_var,
            values=[profile['name'] for profile in PRICE_PROFILES.values()],
            state='readonly',
            font=self.fonts['body'],
            width=20
        )
        self.profile_combo.pack(side='left', padx=5)
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_change)
        
        # Información del perfil actual
        self.profile_info = tk.Label(
            pricing_frame,
            text="",
            font=self.fonts['body'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_light']
        )
        self.profile_info.pack(pady=(0, 10))
        
        self.update_profile_info()
    
    def create_history_section(self, parent):
        """Crear la sección de historial rápido"""
        history_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief='raised', bd=2)
        history_frame.pack(fill='both', expand=True)
        
        tk.Label(
            history_frame,
            text="📊 ÚLTIMO VIAJE",
            font=self.fonts['subtitle'],
            fg=self.colors['accent'],
            bg=self.colors['bg_light']
        ).pack(pady=(10, 5))
        
        # Text widget para mostrar último viaje
        self.last_trip_text = tk.Text(
            history_frame,
            height=4,
            width=50,
            font=self.fonts['body'],
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            relief='sunken',
            bd=2,
            state='disabled'
        )
        self.last_trip_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    def toggle_trip(self):
        """Iniciar o finalizar viaje"""
        if not self.trip_active:
            self.start_trip()
        else:
            self.finish_trip()
    
    def start_trip(self):
        """Iniciar un nuevo viaje"""
        self.trip_active = True
        self.start_time = time.time()
        self.current_state_start = time.time()
        self.state = "stopped"
        self.stopped_time = 0
        self.moving_time = 0
        self.timer_running = True
        
        # Actualizar interfaz
        self.start_finish_btn.config(
            text="🏁 FINALIZAR VIAJE",
            bg=self.colors['error']
        )
        self.stop_move_btn.config(state='normal', bg=self.colors['warning'])
        self.status_var.set("🚖 Viaje en curso - PARADO")
        
        logging.info("Viaje iniciado desde GUI")
    
    def finish_trip(self):
        """Finalizar el viaje actual"""
        if not self.trip_active:
            return
        
        # Calcular tiempo final
        self.update_times()
        
        # Calcular tarifa
        total_fare = calculate_fare(self.stopped_time, self.moving_time)
        
        # Guardar en historial
        save_trip_to_history(self.stopped_time, self.moving_time, total_fare)
        
        # Mostrar resumen
        self.show_trip_summary(total_fare)
        
        # Reset
        self.reset_trip()
        
        logging.info(f"Viaje finalizado desde GUI - Tarifa: €{total_fare:.2f}")
    
    def reset_trip(self):
        """Resetear el estado del viaje"""
        self.trip_active = False
        self.timer_running = False
        self.stopped_time = 0
        self.moving_time = 0
        
        # Actualizar interfaz
        self.start_finish_btn.config(
            text="🚀 INICIAR VIAJE",
            bg=self.colors['success']
        )
        self.stop_move_btn.config(
            text="🛑 PARAR",
            bg=self.colors['warning'],
            state='disabled'
        )
        self.status_var.set("🚖 Listo para iniciar viaje")
        self.time_stopped_var.set("0.0")
        self.time_moving_var.set("0.0")
        self.fare_var.set("€0.00")
    
    def toggle_state(self):
        """Cambiar entre parado y movimiento"""
        if not self.trip_active:
            return
        
        # Actualizar tiempos antes del cambio
        self.update_times()
        
        # Cambiar estado
        if self.state == "stopped":
            self.state = "moving"
            self.stop_move_btn.config(
                text="🏃 EN MOVIMIENTO",
                bg=self.colors['success']
            )
            self.status_var.set("🚖 Viaje en curso - EN MOVIMIENTO")
        else:
            self.state = "stopped"
            self.stop_move_btn.config(
                text="🛑 PARADO",
                bg=self.colors['warning']
            )
            self.status_var.set("🚖 Viaje en curso - PARADO")
        
        # Reiniciar contador para el nuevo estado
        self.current_state_start = time.time()
        
        logging.info(f"Estado cambiado a: {self.state}")
    
    def update_times(self):
        """Actualizar los tiempos acumulados"""
        if not self.trip_active:
            return
        
        current_time = time.time()
        duration = current_time - self.current_state_start
        
        if self.state == "stopped":
            self.stopped_time += duration
        else:
            self.moving_time += duration
        
        self.current_state_start = current_time
    
    def update_timer(self):
        """Actualizar el timer y la interfaz"""
        if self.timer_running and self.trip_active:
            self.update_times()
            
            # Actualizar display de tiempos
            self.time_stopped_var.set(f"{self.stopped_time:.1f}")
            self.time_moving_var.set(f"{self.moving_time:.1f}")
            
            # Calcular tarifa estimada
            profile = PRICE_PROFILES[taximeter_main.CURRENT_PROFILE]
            estimated_fare = (self.stopped_time * profile["stopped"] + 
                             self.moving_time * profile["moving"])
            self.fare_var.set(f"€{estimated_fare:.2f}")
            
            # Reiniciar el contador actual
            self.current_state_start = time.time()
        
        # Programar siguiente actualización
        self.root.after(100, self.update_timer)
    
    def on_profile_change(self, event):
        """Manejar cambio de perfil de tarifa"""
        selected_name = self.profile_var.get()
        
        # Encontrar el key del perfil seleccionado
        for key, profile in PRICE_PROFILES.items():
            if profile['name'] == selected_name:
                change_price_profile(key)
                break
        
        self.update_profile_info()
        logging.info(f"Perfil cambiado a: {selected_name}")
    
    def update_profile_info(self):
        """Actualizar la información del perfil actual"""
        profile = PRICE_PROFILES[taximeter_main.CURRENT_PROFILE]
        info_text = f"Parado: €{profile['stopped']}/s | Movimiento: €{profile['moving']}/s"
        self.profile_info.config(text=info_text)
        
        # Actualizar combobox
        self.profile_var.set(profile['name'])
    
    def show_trip_summary(self, total_fare):
        """Mostrar resumen del viaje"""
        summary = f"""
╔══════════════════════════════════════╗
║            RESUMEN DEL VIAJE          ║
╠══════════════════════════════════════╣
║ 🛑 Tiempo parado:    {self.stopped_time:>8.1f}s ║
║ 🏃 Tiempo movimiento: {self.moving_time:>8.1f}s ║
║ ⏱️  Tiempo total:     {(self.stopped_time + self.moving_time):>8.1f}s ║
║ 💰 Tarifa total:     {total_fare:>9.2f}€ ║
╚══════════════════════════════════════╝
        """
        
        messagebox.showinfo("🚖 Viaje Finalizado", summary)
        
        # Actualizar último viaje en la interfaz
        self.last_trip_text.config(state='normal')
        self.last_trip_text.delete('1.0', tk.END)
        self.last_trip_text.insert('1.0', summary)
        self.last_trip_text.config(state='disabled')
    
    def show_history(self):
        """Mostrar ventana de historial completo"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Historial de Viajes")
        history_window.geometry("600x400")
        history_window.configure(bg=self.colors['bg_dark'])
        
        # Centrar ventana
        history_window.transient(self.root)
        history_window.grab_set()
        
        # Texto del historial
        history_text = tk.Text(
            history_window,
            font=('Consolas', 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            relief='raised',
            bd=2
        )
        history_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side='right', fill='y')
        history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=history_text.yview)
        
        # Cargar historial
        try:
            if os.path.exists('logs/historial_viajes.txt'):
                with open('logs/historial_viajes.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                if content:
                    history_text.insert('1.0', content)
                else:
                    history_text.insert('1.0', "📭 No hay viajes en el historial aún.")
            else:
                history_text.insert('1.0', "📭 No hay viajes en el historial aún.")
        except Exception as e:
            history_text.insert('1.0', f"❌ Error leyendo historial: {e}")
        
        history_text.config(state='disabled')
    
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        if self.trip_active:
            # Confirmar si hay un viaje activo
            if messagebox.askquestion(
                "🚖 Viaje Activo", 
                "Hay un viaje en curso.\n¿Deseas finalizarlo antes de cerrar?",
                icon='warning'
            ) == 'yes':
                self.finish_trip()
        
        # Cerrar aplicación
        logging.info("🛑 Cerrando Digital Taximeter GUI")
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

def main():
    """Función principal para ejecutar la GUI"""
    try:
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/taximeter_gui.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        
        print("🚖 Iniciando Digital Taximeter GUI...")
        print("   - Interfaz gráfica profesional")
        print("   - Control de viajes en tiempo real") 
        print("   - Múltiples perfiles de tarifa")
        print("   - Historial integrado")
        print("✅ Abriendo ventana principal...")
        
        # Iniciar aplicación
        logging.info("🚀 Iniciando Digital Taximeter GUI")
        app = TaximeterGUI()
        app.run()
        
        print("🏁 GUI cerrada correctamente")
        logging.info("🛑 Digital Taximeter GUI cerrada")
        
    except Exception as e:
        print(f"❌ Error iniciando GUI: {e}")
        logging.error(f"Error crítico en GUI: {e}")
        raise

if __name__ == "__main__":
    main()
