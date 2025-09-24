"""Definición de la clase Auto como subclase de Vehiculo."""

from .vehiculo_base import Vehiculo


class Auto(Vehiculo):
    """Representa un automóvil disponible para alquiler."""

    def __init__(self, nombre: str):
        """Inicializa un auto con su nombre y tarifa por hora en COP."""
        super().__init__(nombre=nombre, tarifa_hora=20000)

    def calcular_costo(self, horas: int) -> int:
        """Calcula el costo del alquiler en función de las horas."""
        return self.tarifa_hora * horas

    def __str__(self):
        """Devuelve una representación en texto del auto."""
        return f"{self.nombre} (Auto) - {self.tarifa_hora:,.0f} COP/hora"
