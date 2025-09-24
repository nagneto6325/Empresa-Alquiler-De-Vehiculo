"""Definición de la clase Moto como subclase de Vehiculo."""

from .vehiculo_base import Vehiculo

class Moto(Vehiculo):
    """Representa una motocicleta disponible para alquiler."""

    def __init__(self, nombre, cilindraje: int = 150, casco_obligatorio: bool = True):
        """Inicializa una motocicleta con cilindraje, tarifa por hora y si requiere casco."""
        super().__init__(nombre, tarifa_hora=50000)
        self.cilindraje = cilindraje
        self.casco_obligatorio = casco_obligatorio

    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo del alquiler con un 20% adicional si la moto supera 500cc."""
        costo = self.tarifa_hora * horas
        if self.cilindraje > 500:
            costo *= 1.2
        return costo

    def __str__(self):
        """Devuelve una representación en texto de la moto."""
        return f"{self.nombre} ({self.cilindraje}cc) - {self.tarifa_hora:,.0f} COP/hora"
