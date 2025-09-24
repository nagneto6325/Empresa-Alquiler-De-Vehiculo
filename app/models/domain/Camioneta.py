"""Definición de la clase Camioneta como subclase de Vehiculo."""

from .vehiculo_base import Vehiculo


class Camioneta(Vehiculo):
    """Representa una camioneta disponible para alquiler."""

    def __init__(self, nombre: str, capacidad_carga: int = 500):
        """Inicializa una camioneta con capacidad de carga y tarifa por hora."""
        super().__init__(nombre, tarifa_hora=120000)
        self.capacidad_carga = capacidad_carga

    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo con un 20% extra si la carga supera los 1000 kg."""
        costo = self.tarifa_hora * horas
        if self.capacidad_carga > 1000:
            costo *= 1.2
        return costo

    def __str__(self):
        """Devuelve una representación en texto de la camioneta."""
        return (
            f"{self.nombre} (Carga: {self.capacidad_carga}kg) - "
            f"{self.tarifa_hora:,.0f} COP/hora"
        )
