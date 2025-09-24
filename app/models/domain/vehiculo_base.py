"""Definicion de la jerarquia de vehiculos disponibles en el sistema de alquiler."""

from abc import ABC, abstractmethod


class Vehiculo(ABC):
    """Clase abstracta que define los atributos y metodos basicos de un vehiculo."""

    def __init__(self, nombre: str, tarifa_hora: float, disponible: bool = True):
        """Inicializa un vehiculo con nombre, tarifa por hora y estado de disponibilidad."""
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        """Metodo abstracto que cada subclase debe implementar para calcular el costo."""
        pass

    def __str__(self):
        """Devuelve una representacion en texto del vehiculo."""
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"{self.nombre} | Tarifa: {self.tarifa_hora:,.0f} COP/hora | {estado}"