"""Sistema de alquiler de vehiculos con auditoria completa."""

from datetime import datetime, timedelta
from database import SessionLocal
from app.models.orm.Vehiculo import Vehiculo
from app.models.orm.Contrato import Contrato
from app.models.orm.Pago import Pago
from app.models.orm.Mantenimiento import Mantenimiento
import random


class SistemaAlquiler:
    """Sistema principal de gestion de alquiler de vehiculos."""

    def __init__(self, cliente, usuario_id):
        """
        Inicializa el sistema de alquiler.
        
        Args:
            cliente: Objeto Cliente que usa el sistema
            usuario_id: ID del usuario autenticado
        """
        self.cliente = cliente
        self.usuario_id = usuario_id

    def menu_principal(self):
        """Muestra el menu principal y gestiona las opciones del usuario."""
        while True:
            print("\n" + "=" * 30)
            print("MENU DE ALQUILER")
            print("=" * 30)
            print("1. Ver vehiculos disponibles")
            print("2. Alquilar vehiculo")
            print("3. Devolver vehiculo")
            print("4. Ver mis contratos")
            print("5. Ver mis pagos")
            print("6. Ver mantenimientos")
            print("7. Salir")

            opcion = input("\nSeleccione una opcion: ").strip()

            if opcion == "1":
                self.listar_vehiculos()
            elif opcion == "2":
                self.alquilar_vehiculo()
            elif opcion == "3":
                self.devolver_vehiculo()
            elif opcion == "4":
                self.ver_contratos()
            elif opcion == "5":
                self.ver_pagos()
            elif opcion == "6":
                self.ver_mantenimientos()
            elif opcion == "7":
                print("Cerrando sesion...")
                break
            else:
                print("Opcion invalida")

    def listar_vehiculos(self):
        """Lista todos los vehiculos disponibles para alquiler."""
        db = SessionLocal()
        try:
            vehiculos = (
                db.query(Vehiculo)
                .filter(
                    Vehiculo.disponible == True, Vehiculo.necesita_mantenimiento == False
                )
                .all()
            )

            print(f"\n--- VEHICULOS DISPONIBLES ({len(vehiculos)}) ---")

            if not vehiculos:
                print("No hay vehiculos disponibles en este momento.")
                return

            for i, v in enumerate(vehiculos, 1):
                detalles = self._obtener_detalles_vehiculo(v)
                print(f"{i}. {v.nombre} | {v.tipo}{detalles} | ${v.tarifa_hora:,}/hora")
                print(f"   Creado: {v.fecha_creacion.strftime('%d/%m/%Y')}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()

    def _obtener_detalles_vehiculo(self, vehiculo):
        """
        Obtiene detalles especificos del vehiculo segun su tipo.
        
        Args:
            vehiculo: Objeto Vehiculo del cual obtener detalles
            
        Returns:
            str: Cadena con detalles especificos del vehiculo
        """
        if vehiculo.tipo == "Auto" and vehiculo.puertas:
            return f" | {vehiculo.puertas} puertas"
        elif vehiculo.tipo == "Moto" and vehiculo.cilindraje:
            return f" | {vehiculo.cilindraje}cc"
        elif vehiculo.tipo == "Camioneta" and vehiculo.capacidad_carga:
            return f" | Carga: {vehiculo.capacidad_carga}kg"
        elif vehiculo.tipo == "Bicicleta" and vehiculo.tipo_bici:
            return f" | Tipo: {vehiculo.tipo_bici}"
        elif vehiculo.tipo == "Patineta" and vehiculo.autonomia_km:
            return f" | Autonomia: {vehiculo.autonomia_km}km"
        return ""

    def alquilar_vehiculo(self):
        """Proceso completo de alquiler de un vehiculo."""
        db = SessionLocal()
        try:
            vehiculos = (
                db.query(Vehiculo)
                .filter(
                    Vehiculo.disponible == True, Vehiculo.necesita_mantenimiento == False
                )
                .all()
            )

            if not vehiculos:
                print("No hay vehiculos disponibles para alquilar.")
                return

            print("\n--- ALQUILAR VEHICULO ---")
            for i, v in enumerate(vehiculos, 1):
                detalles = self._obtener_detalles_vehiculo(v)
                print(f"{i}. {v.nombre} | ${v.tarifa_hora:,}/hora{detalles}")

            try:
                opcion = int(input("\nSeleccione el vehiculo (numero): ")) - 1
                if opcion < 0 or opcion >= len(vehiculos):
                    print("Seleccion invalida.")
                    return
            except ValueError:
                print("Debe ingresar un numero valido.")
                return

            vehiculo = vehiculos[opcion]

            try:
                horas = int(input("Horas de alquiler: "))
                if horas <= 0:
                    print("Las horas deben ser mayores a 0.")
                    return
            except ValueError:
                print("Debe ingresar un numero valido.")
                return

            precio_total = vehiculo.tarifa_hora * horas

            print(f"\n--- PAGO DEL ALQUILER ---")
            print(f"Vehiculo: {vehiculo.nombre}")
            print(f"Horas: {horas}")
            print(f"Total a pagar: ${precio_total:,} COP")

            print("\nMetodos de pago disponibles:")
            print("1. Efectivo")
            print("2. Tarjeta credito/debito")
            print("3. Transferencia bancaria")

            try:
                metodo_opcion = int(input("Seleccione metodo de pago: "))
                metodos = {1: "Efectivo", 2: "Tarjeta", 3: "Transferencia"}
                metodo_pago = metodos.get(metodo_opcion, "Efectivo")
            except ValueError:
                metodo_pago = "Efectivo"

            confirmar = (
                input(
                    f"\nConfirmar pago de ${precio_total:,} COP con {metodo_pago}? (s/n): "
                )
                .strip()
                .lower()
            )
            if confirmar != "s":
                print("Pago cancelado. Alquiler no realizado.")
                return

            fecha_inicio = datetime.utcnow()

            contrato = Contrato(
                cliente_id=self.cliente.id,
                vehiculo_id=vehiculo.id,
                horas_contratadas=horas,
                precio_por_hora=vehiculo.tarifa_hora,
                precio_total=precio_total,
                pagado=True,
                fecha_inicio=fecha_inicio,
                fecha_fin_estimada=fecha_inicio + timedelta(hours=horas),
                id_usuario_creacion=self.usuario_id,
                id_usuario_edicion=self.usuario_id,
            )

            db.add(contrato)
            db.flush()

            pago = Pago(
                contrato_id=contrato.id,
                cliente_id=self.cliente.id,
                monto=precio_total,
                metodo_pago=metodo_pago,
                fecha_pago=datetime.utcnow(),
                estado="Completado",
                id_usuario_creacion=self.usuario_id,
                id_usuario_edicion=self.usuario_id,
            )

            vehiculo.disponible = False
            vehiculo.id_usuario_edicion = self.usuario_id

            db.add(pago)
            db.commit()

            print(f"\nALQUILER Y PAGO EXITOSOS")
            print(f"Vehiculo: {vehiculo.nombre}")
            print(f"Horas: {horas}")
            print(f"Total pagado: ${precio_total:,} COP")
            print(f"Metodo: {metodo_pago}")
            print(f"Inicio: {fecha_inicio.strftime('%d/%m/%Y %H:%M')}")
            print(
                f"Devolucion: {contrato.fecha_fin_estimada.strftime('%d/%m/%Y %H:%M')}"
            )

        except Exception as e:
            print(f"Error al alquilar: {e}")
            db.rollback()
        finally:
            db.close()

    def devolver_vehiculo(self):
        """Proceso de devolucion de un vehiculo alquilado."""
        db = SessionLocal()
        try:
            contratos_activos = (
                db.query(Contrato)
                .filter(
                    Contrato.cliente_id == self.cliente.id,
                    Contrato.fecha_fin_real == None,
                )
                .all()
            )

            if not contratos_activos:
                print("No tienes vehiculos alquilados actualmente.")
                return

            print("\n--- DEVOLVER VEHICULO ---")
            for i, contrato in enumerate(contratos_activos, 1):
                vehiculo = (
                    db.query(Vehiculo).filter(Vehiculo.id == contrato.vehiculo_id).first()
                )
                if vehiculo:
                    inicio = contrato.fecha_inicio.strftime("%d/%m %H:%M")
                    print(
                        f"{i}. {vehiculo.nombre} (desde {inicio}) - ${contrato.precio_total:,}"
                    )

            try:
                opcion = int(input("\nSeleccione vehiculo a devolver: ")) - 1
                if opcion < 0 or opcion >= len(contratos_activos):
                    print("Seleccion invalida.")
                    return
            except ValueError:
                print("Debe ingresar un numero.")
                return

            contrato = contratos_activos[opcion]
            vehiculo = (
                db.query(Vehiculo).filter(Vehiculo.id == contrato.vehiculo_id).first()
            )

            if not vehiculo:
                print("Error: Vehiculo no encontrado.")
                return

            horas_contratadas = contrato.horas_contratadas
            horas_reales = (
                datetime.utcnow() - contrato.fecha_inicio
            ).total_seconds() / 3600

            cargo_extra = 0
            if horas_reales > horas_contratadas:
                horas_extra = horas_reales - horas_contratadas
                cargo_extra = horas_extra * contrato.precio_por_hora * 1.2
                print(
                    f"Horas extras: {horas_extra:.1f}h - Cargo adicional: ${cargo_extra:,.0f} COP"
                )

                confirmar = (
                    input("Aceptar cargo por horas extras? (s/n): ").strip().lower()
                )
                if confirmar == "s":
                    pago_extra = Pago(
                        contrato_id=contrato.id,
                        cliente_id=self.cliente.id,
                        monto=cargo_extra,
                        metodo_pago="Efectivo",
                        fecha_pago=datetime.utcnow(),
                        estado="Completado",
                        id_usuario_creacion=self.usuario_id,
                        id_usuario_edicion=self.usuario_id,
                    )
                    db.add(pago_extra)
                    print(f"Pago por horas extras registrado: ${cargo_extra:,.0f} COP")
                else:
                    cargo_extra = 0

            contrato.fecha_fin_real = datetime.utcnow()
            contrato.id_usuario_edicion = self.usuario_id

            vehiculo.disponible = False
            vehiculo.necesita_mantenimiento = True
            vehiculo.id_usuario_edicion = self.usuario_id

            tipos_mantenimiento = [
                "Limpieza basica",
                "Revision general",
                "Limpieza completa",
            ]
            costo_mantenimiento = random.randint(5000, 20000)

            mantenimiento = Mantenimiento(
                vehiculo_id=vehiculo.id,
                contrato_id=contrato.id,
                tipo=random.choice(tipos_mantenimiento),
                descripcion=f"Mantenimiento post-alquiler de {vehiculo.nombre}",
                costo=costo_mantenimiento,
                fecha_solicitud=datetime.utcnow(),
                estado="Pendiente",
                id_usuario_creacion=self.usuario_id,
                id_usuario_edicion=self.usuario_id,
            )

            db.add(mantenimiento)
            db.commit()

            print(f"\nVEHICULO DEVUELTO EXITOSAMENTE")
            print(f"Vehiculo: {vehiculo.nombre}")
            print(f"Tiempo total: {horas_reales:.1f}h")
            print(f"Total pagado: ${contrato.precio_total + cargo_extra:,.0f} COP")
            print(f"Enviado a mantenimiento: {mantenimiento.tipo}")
            if cargo_extra > 0:
                print(f"Cargo extra: ${cargo_extra:,.0f} COP")

        except Exception as e:
            print(f"Error al devolver: {e}")
            db.rollback()
        finally:
            db.close()

    def ver_contratos(self):
        """Muestra todos los contratos del cliente actual."""
        db = SessionLocal()
        try:
            contratos = (
                db.query(Contrato).filter(Contrato.cliente_id == self.cliente.id).all()
            )
            print(f"\n--- MIS CONTRATOS ({len(contratos)}) ---")

            if not contratos:
                print("No tienes contratos registrados.")
                return

            for contrato in contratos:
                vehiculo = (
                    db.query(Vehiculo).filter(Vehiculo.id == contrato.vehiculo_id).first()
                )
                if not vehiculo:
                    continue

                estado = "ACTIVO" if contrato.fecha_fin_real is None else "FINALIZADO"
                fecha_fin = contrato.fecha_fin_real or contrato.fecha_fin_estimada

                total_pagos = (
                    db.query(Pago).filter(Pago.contrato_id == contrato.id).all()
                )
                total_pagado = sum(pago.monto for pago in total_pagos)

                print(f"• {vehiculo.nombre} ({vehiculo.tipo})")
                print(f"  {contrato.horas_contratadas}h | ${total_pagado:,} pagados")
                print(
                    f"  Creacion: {contrato.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
                )
                print(f"  Fin: {fecha_fin.strftime('%d/%m/%Y %H:%M')}")
                print(
                    f"  {estado} | Ultima edicion: {contrato.fecha_actualizacion.strftime('%d/%m/%Y %H:%M')}\n"
                )

        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()

    def ver_pagos(self):
        """Muestra el historial de pagos del cliente."""
        db = SessionLocal()
        try:
            pagos = (
                db.query(Pago)
                .filter(Pago.cliente_id == self.cliente.id)
                .order_by(Pago.fecha_pago.desc())
                .all()
            )
            print(f"\n--- MIS PAGOS ({len(pagos)}) ---")

            if not pagos:
                print("No tienes pagos registrados.")
                return

            total_pagado = 0
            for pago in pagos:
                contrato = (
                    db.query(Contrato).filter(Contrato.id == pago.contrato_id).first()
                )
                vehiculo = None
                if contrato:
                    vehiculo = (
                        db.query(Vehiculo)
                        .filter(Vehiculo.id == contrato.vehiculo_id)
                        .first()
                    )

                nombre_vehiculo = (
                    vehiculo.nombre if vehiculo else "Vehiculo no encontrado"
                )
                tipo_pago = (
                    "PRINCIPAL"
                    if contrato and pago.monto == contrato.precio_total
                    else "EXTRA"
                )

                total_pagado += pago.monto

                print(f"• {nombre_vehiculo} [{tipo_pago}]")
                print(f"  ${pago.monto:,} | {pago.metodo_pago}")
                print(f"  Pago: {pago.fecha_pago.strftime('%d/%m/%Y %H:%M')}")
                print(f"  Estado: {pago.estado}")
                print(f"  Creado por: {pago.id_usuario_creacion}\n")

            print(f"TOTAL PAGADO: ${total_pagado:,} COP")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()

    def ver_mantenimientos(self):
        """Muestra los mantenimientos asociados a los contratos del cliente."""
        db = SessionLocal()
        try:
            mantenimientos = (
                db.query(Mantenimiento)
                .join(Contrato)
                .filter(Contrato.cliente_id == self.cliente.id)
                .all()
            )

            print(f"\n--- MANTENIMIENTOS ({len(mantenimientos)}) ---")

            if not mantenimientos:
                print("No hay mantenimientos registrados para tus alquileres.")
                return

            for mant in mantenimientos:
                vehiculo = (
                    db.query(Vehiculo).filter(Vehiculo.id == mant.vehiculo_id).first()
                )
                contrato = (
                    db.query(Contrato).filter(Contrato.id == mant.contrato_id).first()
                )

                if not vehiculo or not contrato:
                    continue

                estado_icon = (
                    "PENDIENTE"
                    if mant.estado == "Pendiente"
                    else "COMPLETADO"
                    if mant.estado == "Completado"
                    else "CANCELADO"
                )

                print(
                    f"• {vehiculo.nombre} (Alquilado: {contrato.fecha_inicio.strftime('%d/%m/%Y')})"
                )
                print(f"  {mant.tipo} | ${mant.costo:,}")
                print(f"  {mant.descripcion}")
                print(
                    f"  Solicitud: {mant.fecha_solicitud.strftime('%d/%m/%Y %H:%M')}"
                )
                if mant.fecha_completado:
                    print(
                        f"  Completado: {mant.fecha_completado.strftime('%d/%m/%Y %H:%M')}"
                    )
                print(f"  Estado: {estado_icon}")
                print(f"  Creado por: {mant.id_usuario_creacion}\n")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()