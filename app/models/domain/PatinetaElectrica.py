"""Definición de la clase PatinetaElectrica como subclase de Vehiculo."""

from .vehiculo_base import Vehiculo


class PatinetaElectrica(Vehiculo):
    """Representa una patineta eléctrica disponible para alquiler."""

    def __init__(self, nombre: str, autonomia_km: int = 25):
        """Inicializa una patineta eléctrica con autonomía en kilómetros y tarifa por hora."""
        super().__init__(nombre, tarifa_hora=20000)
        self.autonomia_km = autonomia_km

    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo con un 20% extra si la autonomía supera 40 km."""
        costo = self.tarifa_hora * horas
        if self.autonomia_km > 40:
            costo *= 1.2
        return costo

    def __str__(self):
        """Devuelve una representación en texto de la patineta eléctrica."""
        return f"{self.nombre} (Autonomía: {self.autonomia_km}km) - {self.tarifa_hora:,.0f} COP/hora"
