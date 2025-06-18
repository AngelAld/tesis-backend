from Equipos.models import Cpu, Equipo, EstadoEquipo, Memory, Disk, EstadoAlerta
from IA.models import ModeloIA
import numpy as np
import joblib
import tensorflow as tf
from django.contrib.auth import get_user_model
from Notificaciones.models import Notificacion

User = get_user_model()


def identificar_tipo_modelo(modelo: ModeloIA):
    if modelo.archivo.name.endswith(".keras"):
        return "tf"
    elif modelo.archivo.name.endswith(".pkl"):
        return "sklearn"


def predecir(modelo: ModeloIA, datos: list):
    scaler = joblib.load(modelo.scaler.path)

    tipo_modelo = identificar_tipo_modelo(modelo)

    new_data = np.array([datos])

    new_data_scaled = scaler.transform(new_data)

    if tipo_modelo == "sklearn":
        linear_model = joblib.load(modelo.archivo.path)
        predicted_value = linear_model.predict(new_data_scaled)
        return predicted_value[0]
    elif tipo_modelo == "tf":
        nn_model = tf.keras.models.load_model(modelo.archivo.path)  # type: ignore
        predicted_value_nn = nn_model.predict(new_data_scaled).flatten()
        return predicted_value_nn[0]
    else:
        raise ValueError("Modelo no soportado")


def generarAlerta(
    equipo: Equipo,
    cpu: Cpu | None = None,
    memory: Memory | None = None,
    disk: Disk | None = None,
    failure_percentage: float = 0.0,
):
    equipo_estado_score = 0

    estado_alerta, _ = EstadoAlerta.objects.get_or_create(nombre="Sin Alerta")
    if failure_percentage > 5:
        estado_alerta, _ = EstadoAlerta.objects.get_or_create(nombre="Alerta Baja")
    if failure_percentage > 10.0:
        estado_alerta, _ = EstadoAlerta.objects.get_or_create(nombre="Alerta Media")
        equipo_estado_score += 1
    if failure_percentage > 30.0:
        estado_alerta, _ = EstadoAlerta.objects.get_or_create(nombre="Alerta Alta")
        equipo_estado_score += 2
    if failure_percentage > 50.0:
        estado_alerta, _ = EstadoAlerta.objects.get_or_create(nombre="Alerta Crítica")
        equipo_estado_score += 3

    if cpu:
        cpu.estado = estado_alerta
        cpu.save()
    if memory:
        memory.estado = estado_alerta
        memory.save()
    if disk:
        disk.estado = estado_alerta
        disk.save()

    cpus = Cpu.objects.filter(equipo=equipo)
    memories = Memory.objects.filter(equipo=equipo)
    disks = Disk.objects.filter(equipo=equipo)

    if cpus:
        for cpu_item in cpus:
            if cpu_item.estado.nombre == "Alerta Media":
                equipo_estado_score += 1
            elif cpu_item.estado.nombre == "Alerta Alta":
                equipo_estado_score += 2
            elif cpu_item.estado.nombre == "Alerta Crítica":
                equipo_estado_score += 3
    if memories:
        for memory_item in memories:
            if memory_item.estado.nombre == "Alerta Media":
                equipo_estado_score += 1

            elif memory_item.estado.nombre == "Alerta Alta":
                equipo_estado_score += 2
            elif memory_item.estado.nombre == "Alerta Crítica":
                equipo_estado_score += 3
    if disks:
        for disk_item in disks:
            if disk_item.estado.nombre == "Alerta Media":
                equipo_estado_score += 1
            elif disk_item.estado.nombre == "Alerta Alta":
                equipo_estado_score += 2
            elif disk_item.estado.nombre == "Alerta Crítica":
                equipo_estado_score += 3

    if equipo_estado_score < 1:
        equipo.estado_equipo = EstadoEquipo.objects.get_or_create(nombre="Bueno")[0]
    elif equipo_estado_score > 10:
        equipo.estado_equipo = EstadoEquipo.objects.get_or_create(nombre="Regular")[0]
    elif equipo_estado_score > 15:
        equipo.estado_equipo = EstadoEquipo.objects.get_or_create(nombre="Malo")[0]

    if equipo_estado_score < 1:
        equipo.estado_alerta = EstadoAlerta.objects.get_or_create(nombre="Sin alerta")[
            0
        ]

    print("###########################################")
    print(f"Equipo estado score: {equipo_estado_score}")
    print("###########################################")

    if equipo_estado_score > 1:
        equipo.estado_alerta = EstadoAlerta.objects.get_or_create(nombre="Alerta Baja")[
            0
        ]
    elif equipo_estado_score > 10:
        equipo.estado_alerta = EstadoAlerta.objects.get_or_create(
            nombre="Alerta Media"
        )[0]
    elif equipo_estado_score > 15:
        equipo.estado_alerta = EstadoAlerta.objects.get_or_create(nombre="Alerta Alta")[
            0
        ]
    elif equipo_estado_score > 20:
        equipo.estado_alerta = EstadoAlerta.objects.get_or_create(
            nombre="Alerta Crítica"
        )[0]

    equipo.save()

    # Crear notificaciones para administradores según el nivel de alerta
    admins = User.objects.filter(is_superuser=True)
    link = f"http://localhost:5173/equipo/{equipo.pk}/predicciones"
    # Notificación para CPU
    if cpu and equipo_estado_score > 1:
        mensaje = f"Equipo '{equipo.hostname}': CPU '{cpu.nombre}' tiene una {estado_alerta.nombre.lower()}."
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=mensaje,
                link=link,
            )
    # Notificación para Memoria
    if memory and equipo_estado_score > 1:
        mensaje = f"Equipo '{equipo.hostname}': Memoria '{memory.nombre}' tiene una {estado_alerta.nombre.lower()}."
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=mensaje,
                link=link,
            )
    # Notificación para Disco
    if disk and equipo_estado_score > 1:
        mensaje = f"Equipo '{equipo.hostname}': Disco '{disk.nombre}' tiene una {estado_alerta.nombre.lower()}."
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=mensaje,
                link=link,
            )
