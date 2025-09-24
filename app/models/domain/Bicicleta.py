"""Definición de la clase Bicicleta como subclase de Vehiculo."""

from .vehiculo_base import Vehiculo


class Bicicleta(Vehiculo):
    """Representa una bicicleta disponible para alquiler."""

    def __init__(self, nombre: str, tipo: str = "montaña"):
        """Inicializa una bicicleta con tipo y tarifa por hora."""
        super().__init__(nombre, tarifa_hora=15000)
        self.tipo = tipo

    def calcular_costo(self, horas: int) -> float:
        """Calcula el costo con un 30% extra si la bicicleta es eléctrica."""
        costo = self.tarifa_hora * horas
        if self.tipo.lower() == "eléctrica":
            costo *= 1.3
        return costo

    def __str__(self):
        """Devuelve una representación en texto de la bicicleta."""
        return (
            f"{self.nombre} (Bicicleta {self.tipo}) - "
            f"{self.tarifa_hora:,.0f} COP/hora"
        )
