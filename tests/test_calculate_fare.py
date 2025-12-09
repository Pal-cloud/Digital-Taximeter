"""
Tests para la funcionalidad del taxímetro digital.
"""
import unittest
import sys
import os

# Agregar el directorio principal al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import TaxiMeter


class TestTaxiMeterCalculateFare(unittest.TestCase):
    """Tests unitarios para el cálculo de tarifas del taxímetro."""
    
    def setUp(self):
        """Configurar el taxímetro para cada test."""
        self.meter = TaxiMeter()
    
    def test_solo_tiempo_parado(self):
        """Test: Solo tiempo detenido, sin movimiento."""
        self.meter.stopped_time = 100  # 100 segundos parado
        self.meter.moving_time = 0
        resultado = self.meter.calculate_fare()
        esperado = 100 * 0.02  # 2.00€
        self.assertEqual(resultado, esperado)
    
    def test_solo_tiempo_movimiento(self):
        """Test: Solo tiempo en movimiento, sin paradas."""
        self.meter.stopped_time = 0
        self.meter.moving_time = 100  # 100 segundos movimiento
        resultado = self.meter.calculate_fare()
        esperado = 100 * 0.05  # 5.00€
        self.assertEqual(resultado, esperado)
    
    def test_tiempo_mixto(self):
        """Test: Combinación de tiempo parado y en movimiento."""
        self.meter.stopped_time = 60  # 60s parado
        self.meter.moving_time = 120  # 120s movimiento
        resultado = self.meter.calculate_fare()
        esperado = (60 * 0.02) + (120 * 0.05)  # 1.20 + 6.00 = 7.20€
        self.assertEqual(resultado, esperado)
    
    def test_tiempo_cero(self):
        """Test: Sin tiempo parado ni en movimiento."""
        self.meter.stopped_time = 0
        self.meter.moving_time = 0
        resultado = self.meter.calculate_fare()
        esperado = 0.0
        self.assertEqual(resultado, esperado)
    
    def test_numeros_decimales(self):
        """Test: Manejo de números decimales."""
        self.meter.stopped_time = 30.5
        self.meter.moving_time = 45.7
        resultado = self.meter.calculate_fare()
        esperado = round((30.5 * 0.02) + (45.7 * 0.05), 2)  # Resultado redondeado
        self.assertEqual(resultado, esperado)
    
    def test_viaje_corto(self):
        """Test: Viaje muy corto (1 segundo de cada tipo)."""
        self.meter.stopped_time = 1
        self.meter.moving_time = 1
        resultado = self.meter.calculate_fare()
        esperado = (1 * 0.02) + (1 * 0.05)  # 0.02 + 0.05 = 0.07€
        self.assertEqual(resultado, esperado)
    
    def test_viaje_largo(self):
        """Test: Viaje largo (1 hora = 3600 segundos)."""
        self.meter.stopped_time = 1800  # 30 min parado
        self.meter.moving_time = 1800   # 30 min movimiento
        resultado = self.meter.calculate_fare()
        esperado = (1800 * 0.02) + (1800 * 0.05)  # 36 + 90 = 126€
        self.assertEqual(resultado, esperado)


if __name__ == '__main__':
    unittest.main()
