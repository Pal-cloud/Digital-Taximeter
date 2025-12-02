# Digital Taximeter 🚕

```
╔══════════════════════════════════════════════════════════════╗
║                    DIGITAL TAXIMETER                        ║
║                  Sistema de Taxímetro Digital               ║
║                         🚕 v1.0 🚕                          ║
╚══════════════════════════════════════════════════════════════╝
```

Un sistema de taxímetro digital desarrollado en Python que simula el funcionamiento de un taxímetro real con diferentes estados y cálculo de tarifas.

## 📋 Descripción

Digital Taximeter es una aplicación de consola que simula el comportamiento de un taxímetro tradicional. El sistema calcula automáticamente las tarifas basándose en el tiempo que el taxi permanece detenido versus el tiempo que está en movimiento, aplicando tarifas diferenciadas para cada estado.

## 🚀 Características

- **Control de viaje**: Iniciar, pausar y finalizar viajes
- **Estados dinámicos**: Alternar entre estado "detenido" y "en movimiento"
- **Cálculo de tarifas**: Sistema de tarifas diferenciadas por estado
- **Resumen de viaje**: Información detallada al finalizar cada viaje
- **Interfaz intuitiva**: Comandos simples y claros
- **Sistema de logging**: Registro automático de actividades para trazabilidad

## 💰 Sistema de Tarifas

- **Tiempo detenido**: €0.02 por segundo
- **Tiempo en movimiento**: €0.05 por segundo

## 🛠️ Instalación

1. Clona o descarga este repositorio
2. Asegúrate de tener Python 3.6 o superior instalado
3. No se requieren dependencias externas (solo librerías estándar)

## 📖 Uso

Para ejecutar el taxímetro, usa el siguiente comando en la terminal:

```bash
python main.py
```

### Comandos Disponibles

- `start` - Iniciar un nuevo viaje (estado inicial: detenido)
- `stop` - Cambiar el estado a "detenido"
- `move` - Cambiar el estado a "en movimiento"
- `finish` - Finalizar el viaje y mostrar el resumen con la tarifa total
- `exit` - Salir de la aplicación

### Ejemplo de Uso

```
Welcome to Digital Taxi
Available commands:'start', 'stop', 'move', 'finish', 'exit'

> start
Trip started. Initial state: 'stopped'

> move
State changed to 'moving'.

> stop
State changed to 'stopped'.

> finish
Este es el total: 1.25€

--- Trip Summary ---
Stopped time: 15.3 seconds
Moving time: 20.1 seconds
Total fare: €1.31
---------------------
```

## 🏗️ Estructura del Proyecto

```
Digital-Taximeter/
├── main.py           # Archivo principal con la lógica del taxímetro
├── taximeter.ipynb   # Notebook para experimentación (opcional)
├── taximeter.log     # Archivo de logs generado automáticamente
└── README.md         # Este archivo
```

## 🔧 Funciones Principales

### `calculate_fare(seconds_stopped, seconds_moving)`
Calcula la tarifa total basándose en los segundos detenido y en movimiento.

### `taximeter()`
Función principal que maneja la interfaz de usuario y la lógica del taxímetro.

## 📊 Sistema de Logging

El proyecto incluye un sistema de logging simple para la trazabilidad:

- **Archivo de logs**: `taximeter.log` (creado automáticamente)
- **Formato**: Timestamp + mensaje
- **Ubicación**: Mismo directorio del proyecto
- **Salida dual**: Archivo + consola
- **Codificación**: UTF-8 para caracteres especiales

### Eventos Registrados

- Inicio del programa
- Inicio de un viaje
- Salida de la aplicación
- (Futuras expansiones pueden incluir más eventos)

## 🎯 Casos de Uso

- **Educativo**: Aprender sobre sistemas de tiempo real y cálculo de tarifas
- **Simulación**: Entender el funcionamiento de un taxímetro
- **Prototipo**: Base para desarrollar sistemas de facturación más complejos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🛡️ Manejo de Errores

El sistema incluye validaciones para:
- Intentar usar comandos sin haber iniciado un viaje
- Intentar iniciar un viaje cuando ya hay uno en progreso
- Comandos inválidos con mensajes de ayuda

## 🔮 Futuras Mejoras

- [ ] Interfaz gráfica con tkinter
- [ ] Guardado de historial de viajes
- [ ] Configuración de tarifas personalizables
- [ ] Integración con GPS para detección automática de movimiento
- [ ] Exportación de reportes en CSV/PDF
- [ ] Expansión del sistema de logging para más eventos

---
*Desarrollado con ❤️ en Python*